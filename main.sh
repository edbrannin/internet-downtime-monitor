while true; do
    # Can't install Python packages until the net is back, so let's start by making text files.
    ping -o google.com && (date >> OK.txt) || (echo -n "FAIL "; date | tee -a FAIL.txt)
    sleep 60
done
