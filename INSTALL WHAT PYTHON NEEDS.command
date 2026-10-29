#!/bin/bash
#
# INSTALL WHAT PYTHON NEEDS.command
#
# Double-click this ONCE, on a Mac where nothing in this repo has run before.
#
# It does not install Visual Studio and it does not install Xcode. The dialog
# macOS shows is for the Xcode COMMAND LINE TOOLS: Apple's own, about 600MB,
# and the thing python3 needs before it will start. Click Install and wait.
#
# After that it installs the four Python packages the gates need and checks
# that they actually import. It changes nothing inside the repo.
#

bold=$'\033[1m'; red=$'\033[31m'; grn=$'\033[32m'; ylw=$'\033[33m'; off=$'\033[0m'
cd "$(dirname "$0")" || exit 1

echo
echo "${bold}Setting up Python for the Medicaid Dollar repo${off}"
echo

# --- 1 -------------------------------------------------------------------
echo "${bold}1 of 3  Apple's command line tools${off}"
if xcode-select -p >/dev/null 2>&1; then
  echo "${grn}        already installed${off}"
else
  echo "        Not installed. A dialog will appear now."
  echo "        ${bold}Click Install.${off} It is Apple's, about 600MB, and it is"
  echo "        not Visual Studio. This takes a few minutes."
  xcode-select --install 2>/dev/null
  echo
  read -r -p "        Press return once the installer has FINISHED. "
  if ! xcode-select -p >/dev/null 2>&1; then
    echo "${red}        Still not installed. Nothing else will work until it is.${off}"
    echo; read -r -p "Press return to close."; exit 1
  fi
  echo "${grn}        installed${off}"
fi
echo

# --- 2 -------------------------------------------------------------------
echo "${bold}2 of 3  The Python packages the gates need${off}"
PY=python3
command -v $PY >/dev/null 2>&1 || {
  echo "${red}        python3 still not found. Send me what this printed.${off}"
  echo; read -r -p "Press return to close."; exit 1; }
echo "        using $($PY --version 2>&1) at $(command -v $PY)"
echo
$PY -m pip install --user --upgrade pip >/dev/null 2>&1
$PY -m pip install --user resvg_py pymupdf pillow playwright
PIP=$?
if [ $PIP -ne 0 ]; then
  echo
  echo "${red}        At least one package would not install.${off}"
  echo "        Send me everything above this line. Do not guess at it."
  echo; read -r -p "Press return to close."; exit 1
fi
echo
echo "        Fetching the headless browser the PDF and deck gates drive."
$PY -m playwright install chromium
echo

# --- 3 -------------------------------------------------------------------
echo "${bold}3 of 3  Checking it actually works${off}"
echo
$PY -c "import resvg_py, fitz; print('render deps ok')" 2>&1
A=$?
$PY -c "import playwright, PIL; print('browser and image deps ok')" 2>&1
B=$?
echo
echo "============================================================"
if [ $A -eq 0 ] && [ $B -eq 0 ]; then
  echo "${grn}${bold}Python is ready.${off}"
  echo
  echo "Every .command file in this folder will now run. Start with"
  echo "${bold}FINISH THE 29 OCT UPDATE.command${off}."
else
  echo "${ylw}${bold}Something did not import. Send me the lines above.${off}"
  echo
  echo "This is the useful failure: it names the package, so it is a"
  echo "fixable problem rather than a dialog you have to interpret."
fi
echo "============================================================"
echo
read -r -p "Press return to close."
