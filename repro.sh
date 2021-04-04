#!/usr/bin/env bash

# -Ee ensures script will stop on first command failure (alternatively, use: set -o errexit)
# -u ensures script will exit on first unset variable encountered (alternatively, use: set -o nounset)
# -o pipefail ensures that if any command in a set of piped commands failed, the overall status is that of the failed one
set -Eeuo pipefail

trap cleanup SIGINT SIGTERM ERR EXIT
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

usage() {
cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-v] -s all|phase1|phase2 [test]
Script description here.
Available options:
-h, --help      Print this help and exit
-v, --verbose   Print script debug info
-s, --stage     Pipeline stage. Accepted values: all | phase1 | phase2
test            Optional argument. When passed, will force the use of a subsample
EOF
exit
}

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  # script cleanup here
}

setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
      NOFORMAT='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  else
      NOFORMAT='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}
parse_params() {
  stage=''
  while :; do
  case "${1-}" in
      -h | --help) usage ;;
      -v | --verbose) set -x ;;
      --no-color) NO_COLOR=1 ;;
      -s | --stage)
        stage="${2-}"
  shift
        ;;
      -?*) die "Unknown option: $1" ;;
  *) break ;;
  esac
  shift
  done
  args=("$@")
  # check required params and arguments
  [[ -z "${stage-}" ]] && die "Missing required parameter: stage"
  return 0
}
parse_params "$@"
setup_colors
# script logic here
if [[ ${#args[@]} -gt 0  ]] && [[ ${args[0]} == "test" ]]
then
  msg "${CYAN}Test mode is ON. Using random subsample to reduce computational time.${NOFORMAT}"
fi
if [ "$stage" == "all" ]
then
  msg "${BLUE}Reproducing the full pipeline.${NOFORMAT}"
  bash ph1_1-data_preparation.sh || die "${RED}[Phase 1.1] Failed data preparation.${NOFORMAT}"
  bash ph1_2-tools_execution.sh || die "${RED}[Phase 1.2] Failed tool execution.${NOFORMAT}"
  bash ph1_3-analyses_execution.sh || die "${RED}[Phase 1.3] Failed analyses.${NOFORMAT}"
  bash ph2_1-rep_iyer.sh "${args[0]}" || die "${RED}[Phase 2.1] Failed replication of Iyer et al.${NOFORMAT}"
  bash ph2_2-rep_calefato.sh || die "${RED}[Phase 2.1] Failed replication of Calefato et al..${NOFORMAT}"
  msg "${BLUE}Full pipeline reproduced.${NOFORMAT}"
elif [ "$stage" == "phase1" ]
then
  msg "${GREEN}Reproducing phase 1.${NOFORMAT}"
  bash ph1_1-data_preparation.sh || die "${RED}[Phase 1.1] Failed data preparation.${NOFORMAT}"
  bash ph1_2-tools_execution.sh || die "${RED}[Phase 1.2] Failed tool execution.${NOFORMAT}"
  bash ph1_3-analyses_execution.sh || die "${RED}[Phase 1.3] Failed analyses.${NOFORMAT}"
  msg "${GREEN}Phase 1 completed.${NOFORMAT}"
elif [ "$stage" == "phase2" ]
then
  msg "${PURPLE}Reproducing phase 2.${NOFORMAT}"
  bash ph2_1-rep_iyer.sh "${args[0]}" || die "${RED}[Phase 2.1] Failed replication of Iyer et al.${NOFORMAT}"
  bash ph2_2-rep_calefato.sh || die "${RED}[Phase 2.1] Failed replication of Calefato et al..${NOFORMAT}"
  msg "${PURPLE}Phase 2 completed.${NOFORMAT}"
else
  die "${RED}Invalid stage name: ${stage}.${NOFORMAT}"
fi
