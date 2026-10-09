import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "handover_log.txt")


def read_log(path):
    """Read every line of the log file and return them as a list."""
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def collect_parcels(lines):
    """Turn log lines into an ordered list of IDs and a dict of times."""
    order = []
    parcels = {}
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) != 3:
            continue
        parcel_id = parts[0].strip()
        action = parts[1].strip().upper()
        time = parts[2].strip()
        if action != "CHECKIN" and action != "CHECKOUT":
            continue
        if parcel_id not in parcels:
            order.append(parcel_id)
            parcels[parcel_id] = {"CHECKIN": "MISSING", "CHECKOUT": "MISSING"}
        parcels[parcel_id][action] = time
    return order, parcels


def to_minutes(time_text):
    """Convert 'HH:MM' into minutes since midnight."""
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def build_report(lines):
    """Return the report as a list of output lines."""
    order, parcels = collect_parcels(lines)
    report = []
    problems = 0
    for parcel_id in order:
        checkin = parcels[parcel_id]["CHECKIN"]
        checkout = parcels[parcel_id]["CHECKOUT"]
        if checkin == "MISSING" or checkout == "MISSING":
            problems += 1
            minutes = "UNKNOWN"
        else:
            minutes = str(to_minutes(checkout) - to_minutes(checkin))
        report.append(parcel_id + " IN=" + checkin + " OUT=" + checkout + " MINUTES=" + minutes)
    report.append("PROBLEMS: " + str(problems))
    return report


def main():
    for line in build_report(read_log(LOG_FILE)):
        print(line)


if __name__ == "__main__":
    main()