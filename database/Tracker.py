import datetime as dt


def tracker():
    with open('Sleep_tracker.txt', 'r+') as f:
        # Read the last update time.
        lastActive = f.read()

        # If there is an entry, check the difference between now and the last update time.
        if lastActive:
            lastActive = ' '.join(lastActive.split(' ')[2:4])
            lastActive = dt.datetime.strptime(lastActive, "%d/%m/%Y %H:%M:%S")

            now = dt.datetime.now()

            elapsed = (now - lastActive).total_seconds()

            if elapsed >= 86400:
                now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                f.close()
                with open('Sleep_tracker.txt', 'w') as f:
                    f.write('Last Active: %s' % now)

        # Otherwise, print the time now.
        else:
            now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f.write('Last Active: %s' % now)
    return elapsed
