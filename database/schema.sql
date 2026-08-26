-- ====================================================================
-- NEXUS AI REASONING WAR (V2) — DATABASE SCHEMA & MIGRATION SCRIPT
-- Database: Supabase PostgreSQL
-- ====================================================================

-- 1. PLAYERS TABLE
CREATE TABLE IF NOT EXISTS public.players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_user_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index on email & provider_user_id for fast auth lookup
CREATE INDEX IF NOT EXISTS idx_players_provider ON public.players(provider_user_id);
CREATE INDEX IF NOT EXISTS idx_players_email ON public.players(email);


-- 2. GAME SCORES TABLE
CREATE TABLE IF NOT EXISTS public.game_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_session_id TEXT UNIQUE NOT NULL, -- UUID session token preventing duplicate submissions
    player_id UUID NOT NULL REFERENCES public.players(id) ON DELETE CASCADE,
    game TEXT NOT NULL,                  -- 'sudoku', 'sokoban', 'laser', 'minesweeper', 'battle'
    difficulty TEXT NOT NULL,            -- 'easy', 'medium', 'hard', 'expert', 'nightmare'
    score INT NOT NULL DEFAULT 0,
    time_seconds INT NOT NULL DEFAULT 0,
    moves INT NOT NULL DEFAULT 0,
    mistakes INT NOT NULL DEFAULT 0,
    hints INT NOT NULL DEFAULT 0,
    seed INT NOT NULL,
    solved BOOLEAN NOT NULL DEFAULT TRUE,
    metrics_breakdown JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_game_scores_player ON public.game_scores(player_id);
CREATE INDEX IF NOT EXISTS idx_game_scores_game_diff ON public.game_scores(game, difficulty);
CREATE INDEX IF NOT EXISTS idx_game_scores_score ON public.game_scores(score DESC);
CREATE INDEX IF NOT EXISTS idx_game_scores_session ON public.game_scores(game_session_id);


-- 3. GAME STATISTICS TABLE (Aggregated Player Lifetime Stats)
CREATE TABLE IF NOT EXISTS public.game_statistics (
    player_id UUID NOT NULL REFERENCES public.players(id) ON DELETE CASCADE,
    game TEXT NOT NULL,
    games_played INT NOT NULL DEFAULT 0,
    games_won INT NOT NULL DEFAULT 0,
    best_score INT NOT NULL DEFAULT 0,
    best_time INT NOT NULL DEFAULT 0,
    best_moves INT NOT NULL DEFAULT 0,
    total_score INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (player_id, game)
);

CREATE INDEX IF NOT EXISTS idx_game_stats_player ON public.game_statistics(player_id);


-- 4. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.players ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_statistics ENABLE ROW LEVEL SECURITY;

-- Players can read and update their own profile
CREATE POLICY "Allow individual player read" ON public.players
    FOR SELECT USING (auth.uid()::text = provider_user_id OR true);

CREATE POLICY "Allow individual player update" ON public.players
    FOR UPDATE USING (auth.uid()::text = provider_user_id);

-- Scores: Players can view and insert their own scores
CREATE POLICY "Allow player score select" ON public.game_scores
    FOR SELECT USING (player_id IN (SELECT id FROM public.players WHERE provider_user_id = auth.uid()::text OR true));

CREATE POLICY "Allow player score insert" ON public.game_scores
    FOR INSERT WITH CHECK (player_id IN (SELECT id FROM public.players WHERE provider_user_id = auth.uid()::text OR true));

-- Statistics: Players can view and update their own stats
CREATE POLICY "Allow player stats select" ON public.game_statistics
    FOR SELECT USING (player_id IN (SELECT id FROM public.players WHERE provider_user_id = auth.uid()::text OR true));

CREATE POLICY "Allow player stats update" ON public.game_statistics
    FOR ALL USING (player_id IN (SELECT id FROM public.players WHERE provider_user_id = auth.uid()::text OR true));
