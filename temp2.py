import base64
import datetime
import sys

def decode_resume_token(resume_token: dict):
    """
    Decode a MongoDB change stream resume token.
    Only works for tokens with the '_data' field.
    Returns clusterTime, txn ordinal, and raw bytes.
    """
    if "_data" not in resume_token:
        raise ValueError("Not a valid resume token, missing '_data' field")

    # Step 1: Base64 decode
    raw_bytes = base64.b64decode(resume_token["_data"])

    # Step 2: Extract cluster time (first 8 bytes big-endian int)
    cluster_time_sec = int.from_bytes(raw_bytes[0:8], "big")
    cluster_time = datetime.datetime.utcfromtimestamp(cluster_time_sec)

    # Step 3: Ordinal / increment (next 4 bytes usually)
    ordinal = int.from_bytes(raw_bytes[8:12], "big")

    return {
        "raw_hex": raw_bytes.hex(),
        "cluster_time": cluster_time,
        "ordinal": ordinal,
        "length": len(raw_bytes)
    }


def validate_resume_token(resume_token: dict, oplog_window_hours: int = 24):
    """
    Validate whether a resume token is likely to still be valid
    by checking its clusterTime against oplog/change stream retention.
    (MongoDB itself is the final authority on expiry.)
    """
    details = decode_resume_token(resume_token)

    now = datetime.datetime.utcnow()
    age_hours = (now - details["cluster_time"]).total_seconds() / 3600

    details["age_hours"] = age_hours
    details["within_window"] = age_hours <= oplog_window_hours

    return details


if __name__ == "__main__":
    # Example usage
    # Replace with your actual token from change stream["_id"]
    sample_resume_token = {
        "_data": "826C9A7E5C000000012B022C0100296E5A1004"
    }

    result = validate_resume_token(sample_resume_token, oplog_window_hours=24)

    print("Resume Token Details:")
    for k, v in result.items():
        print(f"{k}: {v}")
