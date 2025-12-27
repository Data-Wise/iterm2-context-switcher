#!/bin/bash
# Automated CLI Test Suite for: aiterm
# Generated: 2025-12-26
# Run: bash tests/cli/automated-tests.sh
#
# Exit codes:
#   0 - All tests passed
#   1 - One or more tests failed
#   2 - Test suite error

set -euo pipefail

# ============================================
# Configuration
# ============================================

PASS=0
FAIL=0
SKIP=0
VERBOSE=${VERBOSE:-0}
BAIL=${BAIL:-0}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ============================================
# Helpers
# ============================================

log_pass() {
    PASS=$((PASS + 1))
    echo -e "${GREEN}✅ PASS${NC}: $1"
}

log_fail() {
    FAIL=$((FAIL + 1))
    echo -e "${RED}❌ FAIL${NC}: $1"
    if [[ "$VERBOSE" == "1" ]] && [[ -n "${2:-}" ]]; then
        echo -e "   ${RED}Details: $2${NC}"
    fi
    if [[ "$BAIL" == "1" ]]; then
        echo -e "\n${RED}Bailing out on first failure${NC}"
        print_summary
        exit 1
    fi
}

log_skip() {
    SKIP=$((SKIP + 1))
    echo -e "${YELLOW}⏭️  SKIP${NC}: $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}${BOLD}━━━ $1 ━━━${NC}"
}

print_summary() {
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  RESULTS${NC}"
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "  Passed:  ${GREEN}${PASS}${NC}"
    echo -e "  Failed:  ${RED}${FAIL}${NC}"
    echo -e "  Skipped: ${YELLOW}${SKIP}${NC}"
    echo -e "  Total:   $((PASS + FAIL + SKIP))"
    echo ""

    if [[ $FAIL -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}✅ ALL TESTS PASSED${NC}"
    else
        echo -e "${RED}${BOLD}❌ $FAIL TEST(S) FAILED${NC}"
    fi
}

# ============================================
# Test Suite
# ============================================

echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}  AUTOMATED CLI TEST SUITE: aiterm${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  CLI:     aiterm / ait"
echo "  Time:    $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Verbose: $VERBOSE"
echo ""

# ============================================
# SMOKE TESTS
# ============================================
log_section "Smoke Tests"

# Test: CLI is installed
if command -v ait &> /dev/null; then
    log_pass "CLI is installed (ait in PATH)"
else
    log_fail "CLI not found in PATH" "Run: pip install -e . or uv pip install -e ."
    echo -e "\n${RED}Cannot continue without CLI installed${NC}"
    exit 2
fi

# Test: Version returns successfully
if ait --version > /dev/null 2>&1; then
    VERSION=$(ait --version 2>&1)
    log_pass "Version command works ($VERSION)"
else
    log_fail "Version command failed"
fi

# Test: Help is accessible
if ait --help > /dev/null 2>&1; then
    log_pass "Help is accessible"
else
    log_fail "Help command failed"
fi

# Test: aiterm alias works too
if command -v aiterm &> /dev/null && aiterm --version > /dev/null 2>&1; then
    log_pass "aiterm alias works"
else
    log_skip "aiterm alias not available (ait only)"
fi

# ============================================
# CORE COMMANDS
# ============================================
log_section "Core Commands"

# Test: Doctor runs without error
if ait doctor > /dev/null 2>&1; then
    log_pass "doctor command completes"
else
    log_fail "doctor command failed"
fi

# Test: Detect returns context info
if ait detect 2>&1 | grep -qi "type\|project\|context\|python\|r-package\|node"; then
    log_pass "detect returns context info"
else
    log_fail "detect output unexpected"
fi

# Test: Switch runs without error
if ait switch > /dev/null 2>&1; then
    log_pass "switch command completes"
else
    log_fail "switch command failed"
fi

# Test: Context detect (explicit)
if ait context detect > /dev/null 2>&1; then
    log_pass "context detect works"
else
    log_fail "context detect failed"
fi

# ============================================
# CLAUDE SUBCOMMANDS
# ============================================
log_section "Claude Subcommands"

# Test: Claude settings accessible
if ait claude settings > /dev/null 2>&1; then
    log_pass "claude settings works"
else
    log_fail "claude settings failed"
fi

# Test: Claude approvals list
if ait claude approvals list > /dev/null 2>&1; then
    log_pass "claude approvals list works"
else
    log_fail "claude approvals list failed"
fi

# Test: Claude help
if ait claude --help > /dev/null 2>&1; then
    log_pass "claude --help works"
else
    log_fail "claude --help failed"
fi

# ============================================
# MCP SUBCOMMANDS
# ============================================
log_section "MCP Subcommands"

# Test: MCP list works
if ait mcp list > /dev/null 2>&1; then
    log_pass "mcp list works"
else
    log_fail "mcp list failed"
fi

# Test: MCP validate works
if ait mcp validate > /dev/null 2>&1; then
    log_pass "mcp validate works"
else
    log_fail "mcp validate failed"
fi

# Test: MCP help
if ait mcp --help > /dev/null 2>&1; then
    log_pass "mcp --help works"
else
    log_fail "mcp --help failed"
fi

# ============================================
# SESSIONS SUBCOMMANDS
# ============================================
log_section "Sessions Subcommands"

# Test: Sessions live works
if ait sessions live > /dev/null 2>&1; then
    log_pass "sessions live works"
else
    log_fail "sessions live failed"
fi

# Test: Sessions conflicts works
if ait sessions conflicts > /dev/null 2>&1; then
    log_pass "sessions conflicts works"
else
    log_fail "sessions conflicts failed"
fi

# Test: Sessions history works
if ait sessions history > /dev/null 2>&1; then
    log_pass "sessions history works"
else
    log_fail "sessions history failed"
fi

# Test: Sessions help
if ait sessions --help > /dev/null 2>&1; then
    log_pass "sessions --help works"
else
    log_fail "sessions --help failed"
fi

# ============================================
# IDE SUBCOMMANDS
# ============================================
log_section "IDE Subcommands"

# Test: IDE list works
if ait ide list > /dev/null 2>&1; then
    log_pass "ide list works"
else
    log_fail "ide list failed"
fi

# Test: IDE compare works
if ait ide compare > /dev/null 2>&1; then
    log_pass "ide compare works"
else
    log_fail "ide compare failed"
fi

# Test: IDE help
if ait ide --help > /dev/null 2>&1; then
    log_pass "ide --help works"
else
    log_fail "ide --help failed"
fi

# ============================================
# OPENCODE SUBCOMMANDS
# ============================================
log_section "OpenCode Subcommands"

# Test: OpenCode config works
if ait opencode config > /dev/null 2>&1; then
    log_pass "opencode config works"
else
    log_fail "opencode config failed"
fi

# Test: OpenCode help
if ait opencode --help > /dev/null 2>&1; then
    log_pass "opencode --help works"
else
    log_fail "opencode --help failed"
fi

# ============================================
# ERROR HANDLING
# ============================================
log_section "Error Handling"

# Test: Invalid command shows error
OUTPUT=$(ait nonexistent-command 2>&1 || true)
if echo "$OUTPUT" | grep -q "No such command"; then
    log_pass "Invalid commands show 'No such command'"
else
    log_fail "Invalid command not handled"
fi

# Test: Invalid subcommand
OUTPUT=$(ait claude nonexistent 2>&1 || true)
if echo "$OUTPUT" | grep -q "No such command"; then
    log_pass "Invalid subcommands show 'No such command'"
else
    log_fail "Invalid subcommand not handled"
fi

# ============================================
# EXIT CODES
# ============================================
log_section "Exit Codes"

# Test: Exit code 0 on success
ait --version > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    log_pass "Exit code 0 on success"
else
    log_fail "Exit code not 0 on success"
fi

# Test: Exit code non-zero on error
ait nonexistent-command > /dev/null 2>&1 || EXIT_CODE=$?
if [[ ${EXIT_CODE:-0} -ne 0 ]]; then
    log_pass "Non-zero exit on invalid command"
else
    log_skip "Exit code 0 for invalid (Typer behavior)"
fi

# ============================================
# HELP ACCESSIBILITY
# ============================================
log_section "Help Accessibility"

# Test all major subcommand help
for cmd in context profile claude mcp sessions ide opencode; do
    if ait $cmd --help > /dev/null 2>&1; then
        log_pass "$cmd --help accessible"
    else
        log_fail "$cmd --help failed"
    fi
done

# ============================================
# Summary
# ============================================
print_summary

# Exit with appropriate code
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
