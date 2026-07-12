#!/bin/bash
# Timer for python-quiz skill
# Usage: timer.sh start | check | stop
#
# start → saves epoch to /tmp/.python_quiz_timer, prints start time HH:MM:SS
# check → prints elapsed seconds and human-readable duration
# stop  → prints elapsed, removes timer file

TIMER_FILE="/tmp/.python_quiz_timer"

case "$1" in
  start)
    date +%s > "$TIMER_FILE"
    echo "started_at=$(date '+%H:%M:%S') epoch=$(cat "$TIMER_FILE")"
    ;;

  check|stop)
    if [ ! -f "$TIMER_FILE" ]; then
      echo "error=no_timer_running"
      exit 1
    fi
    START=$(cat "$TIMER_FILE")
    NOW=$(date +%s)
    ELAPSED=$((NOW - START))
    MINS=$((ELAPSED / 60))
    SECS=$((ELAPSED % 60))

    echo "elapsed_seconds=$ELAPSED elapsed=${MINS}m ${SECS}s"

    if [ "$1" = "stop" ]; then
      rm -f "$TIMER_FILE"
    fi
    ;;

  *)
    echo "Usage: $0 start|check|stop"
    exit 1
    ;;
esac
