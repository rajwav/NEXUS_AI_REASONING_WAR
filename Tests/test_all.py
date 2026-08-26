"""
NEXUS AI REASONING WAR - Unified Test Suite Runner
Runs unit and integration tests across Game Engine, AI Algorithms, ML Pipeline, and 10 Missions.
"""

import unittest
import sys
import os

# Ensure package root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.test_engine import TestGameEngine
from Tests.test_algorithms import TestAIAlgorithms
from Tests.test_ml import TestMachineLearning
from Tests.test_missions import TestMissions
from Tests.test_logic_games import TestLogicGamesSuite
from Tests.test_ai_solvers import TestAISolvers
from Tests.test_v2_auth_and_scoring import TestV2AuthAndScoring


def run_all_tests():
    print("=" * 70)
    print(" NEXUS AI REASONING WAR — COMPLETE SYSTEM VERIFICATION TEST SUITE ")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestGameEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestAIAlgorithms))
    suite.addTests(loader.loadTestsFromTestCase(TestMachineLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestMissions))
    suite.addTests(loader.loadTestsFromTestCase(TestLogicGamesSuite))
    suite.addTests(loader.loadTestsFromTestCase(TestAISolvers))
    suite.addTests(loader.loadTestsFromTestCase(TestV2AuthAndScoring))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f" TOTAL TESTS RUN : {result.testsRun}")
    print(f" SUCCESSES      : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" FAILURES       : {len(result.failures)}")
    print(f" ERRORS         : {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print(">> ALL SYSTEMS NOMINAL: 100% OF TESTS PASSED SUCCESSFULLY! <<")
        return 0
    else:
        print(">> CRITICAL TEST FAILURE DETECTED! <<")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
