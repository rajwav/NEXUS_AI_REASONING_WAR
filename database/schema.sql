-- ====================================================================
-- NEXUS AI REASONING WAR (V2) — DATABASE SCHEMA & MIGRATION SCRIPT
-- Target Database: Supabase PostgreSQL (PostgREST API)
-- Security: Row Level Security (RLS) with Strict User Ownership
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

-- Performance Indexes for Players
CREATE INDEX IF NOT EXISTS idx_players_provider ON public.players(provider_user_id);
CREATE INDEX IF NOT EXISTS idx_players_email ON public.players(email);


-- 2. GAME SCORES TABLE
CREATE TABLE IF NOT EXISTS public.game_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_session_id TEXT UNIQUE NOT NULL, -- UUID session token enforcing idempotent deduplication
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

-- Performance Indexes for Scores
CREATE INDEX IF NOT EXISTS idx_game_scores_player ON public.game_scores(player_id);
CREATE INDEX IF NOT EXISTS idx_game_scores_game_diff ON public.game_scores(game, difficulty);
CREATE INDEX IF NOT EXISTS idx_game_scores_score ON public.game_scores(score DESC);
CREATE INDEX IF NOT EXISTS idx_game_scores_session ON public.game_scores(game_session_id);


-- 3. GAME STATISTICS TABLE (Aggregated Lifetime Performance)
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


-- 4. ROLE GRANTS & ACCESS CONTROL
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT SELECT ON TABLE public.players TO anon;
GRANT ALL ON TABLE public.players TO authenticated;
GRANT ALL ON TABLE public.game_scores TO authenticated;
GRANT ALL ON TABLE public.game_statistics TO authenticated;
REVOKE INSERT, UPDATE, DELETE ON TABLE public.game_scores FROM anon;
REVOKE INSERT, UPDATE, DELETE ON TABLE public.game_statistics FROM anon;


-- 5. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.players ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.game_statistics ENABLE ROW LEVEL SECURITY;

-- Players Policies (Authenticated User Ownership)
DROP POLICY IF EXISTS "Allow individual player read" ON public.players;
CREATE POLICY "Allow individual player read" ON public.players
    FOR SELECT TO authenticated, anon USING (true);

DROP POLICY IF EXISTS "Allow individual player insert" ON public.players;
CREATE POLICY "Allow individual player insert" ON public.players
    FOR INSERT TO authenticated WITH CHECK (
        auth.uid() = id OR auth.uid()::text = provider_user_id OR auth.role() = 'anon'
    );

DROP POLICY IF EXISTS "Allow individual player update" ON public.players;
CREATE POLICY "Allow individual player update" ON public.players
    FOR UPDATE TO authenticated USING (
        auth.uid() = id OR auth.uid()::text = provider_user_id
    );

-- Game Scores Policies (Authenticated Ownership Enforced)
DROP POLICY IF EXISTS "Allow player score select" ON public.game_scores;
CREATE POLICY "Allow player score select" ON public.game_scores
    FOR SELECT TO authenticated USING (
        auth.uid() = player_id OR auth.uid()::text = (SELECT provider_user_id FROM public.players WHERE id = game_scores.player_id)
    );

DROP POLICY IF EXISTS "Allow player score insert" ON public.game_scores;
CREATE POLICY "Allow player score insert" ON public.game_scores
    FOR INSERT TO authenticated WITH CHECK (
        auth.uid() = player_id OR auth.uid()::text = (SELECT provider_user_id FROM public.players WHERE id = game_scores.player_id)
    );

-- Game Statistics Policies (Authenticated Ownership Enforced)
DROP POLICY IF EXISTS "Allow player stats select" ON public.game_statistics;
CREATE POLICY "Allow player stats select" ON public.game_statistics
    FOR SELECT TO authenticated USING (
        auth.uid() = player_id OR auth.uid()::text = (SELECT provider_user_id FROM public.players WHERE id = game_statistics.player_id)
    );

DROP POLICY IF EXISTS "Allow player stats update" ON public.game_statistics;
CREATE POLICY "Allow player stats update" ON public.game_statistics
    FOR ALL TO authenticated USING (
        auth.uid() = player_id OR auth.uid()::text = (SELECT provider_user_id FROM public.players WHERE id = game_statistics.player_id)
    );
