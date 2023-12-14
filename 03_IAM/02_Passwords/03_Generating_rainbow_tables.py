# Load the NIST list of 10,000 most commonly used passwords
with open('01_Brute_force_example/nist_10000.txt', newline='') as bad_passwords:
    nist_bad = bad_passwords.read().split('\n')
print(nist_bad[1:10],'\n')

# The following data is a normalized simplified user table
# Imagine this information was stolen or leaked
leaked_users_table = {
    'jamie': {
        'username': 'jamie',
        'role': 'subscriber',
        'md5': '203ad5ffa1d7c650ad681fdff3965cd2'
    }, 
    'amanda': {
        'username': 'amanda',
        'role': 'administrator',
        'md5': '315eb115d98fcbad39ffc5edebd669c9'
    }, 
    'chiaki': {
        'username': 'chiaki',
        'role': 'subscriber',
        'md5': '941c76b34f8687e46af0d94c167d1403'
    }, 
    'viraj': {
        'username': 'viraj',
        'role': 'employee',
        'md5': '319f4d26e3c536b5dd871bb2c52e3178'
    },
}

# import the hashlib
import hashlib 
# example hash
word = 'blueberry'
hashlib.md5(word.encode()).hexdigest()


# Create a rainbow table
# @TODO
# 1. Create a python dictionary for each word in the nist_bad list. For each word, the dictionary should use the hashlib.md5 string as a key, and the word as the value.
# 2. Iterate over each user in the leaked_users_table dictionary and attempt to use the rainbow table to crack their password.

rainbow_table = {}
for i,word in enumerate(nist_bad):
    rainbow_table['decrypted'] = word
    md5_enc = hashlib.md5(word.encode()).hexdigest()
    rainbow_table['md5'] = hashlib.md5(word.encode()).hexdigest()
    rainbow_table[md5_enc] = word

for keys,values in leaked_users_table.items():
    try:
        print(f"The password for {keys} is `{rainbow_table[values['md5']]}`")
    except:
        print('No match')