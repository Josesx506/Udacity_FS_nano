# Import the Python Library
import sys
import bcrypt

password = b"learningisfun"

# Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)

# Check a plain text string against the salted, hashed digest
# check = bcrypt.checkpw(password, hashed)

# @TODO - check with password matches this has key below
hash_keys = b'$2b$14$EFOxm3q8UWH8ZzK1h.WTZeRcPyr8/X0vRfuL3/e9z7AKIMnocurBG'
check = bcrypt.checkpw(password, hash_keys)

print(check)