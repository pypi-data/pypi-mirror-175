![Python build & test](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-11/actions/workflows/build.yaml/badge.svg)

# passwordManagerByAscii Package
A pacakge that can generate, validate, encode, and decode passwords. built with build using setuptools, uploaded to PyPI using twine, and distributed via pip.

Checkout our package [at pypi](https://pypi.org/project/passwordManagerByAscii/0.2.3/)

## Authors
- Victoria Zhang: [Github](https://github.com/Ruixi-Zhang)
- Jenny Shen: [Github](https://github.com/JennyShen10792)
- Tiffany Lee: [Github](https://github.com/les5185)
- Seok Tae Kim: [Github](https://github.com/seoktaekim)
- Khalifa AlFalasi: [Github](https://github.com/Khalifa-AlFalasi)

## Functions
### Validate Password
- The 'validate_password' function can test if the user generated password is valid. 
- In this package, there are two ways for users to generate password. 
    1. Users can use the generate password function to generate a random password that meets the requirement
    2. Users can type in their own password and check if the user generated password is valid. 
- Validate function is applicable for #2. 
- When users generate a password, it checks if the password is at least 6 characters, contains at least 1 special character, 1 number, and 1 capital alphabet to maintain security. 
    ```python
    from passwordManagerByAscii import validate
    # the parameter would take the user input
    validate = validate.validate_pasword('Password123@')
    ```

### Generate Password
- The `generate_password` function can generate a random password within length 6 to 15. The password is guarantee meet the requirement above.
- Generate a password given a length. Note: if the length is greater than 15 or lower than 6. It will generate a random password  within the 6 and 15 range.
    ```python
    from passwordManagerByAscii import generator
    password = generator.generate_password(10)
    ```
- Generate a password without specifying length. Will generate a password with random length within 6 and 15 range.
    ```python
    from passwordManagerByAscii import generator
    password = generator.generate_password()
    ```
### Encode Password
- The `encode_password` function can encrypt a password with any length.
- The encryption follows the following rules given a string: 
	1. reverse the string
	2. swap the char pairs
	3. add dec by their (index+1), then (2(index+1), then 3(index+1) 3 times (3 character per string)
	Note: if the calculated value is over 126 then loop to 33 again by adding on the remainder.
	```python
    from passwordManagerByAscii import encrypt
    encrypted = encrypt.encode_password("hello")
    ```
### Decode Password
- The `decode_password` function can decrypt an encrypted password that is created by the `encode_password` function. 
- Function takes in a string type and will raise error if unmatched types are given.
- Function will also raise error if the value in the string either does not match encryption format, or if any of the character is not in the decimal range of 33 to 126. 
- Function returns a decoded string.
    ```python
    from passwordManagerByAscii import decoder, encrypt
    encrypted_password = encrypt.encode_password('hello')
    decoded_password= decoder.decode_password(encrypted_password)
    #decoded_password is 'hello'
    ```

## How to Install and use the Package
1. Create a ```pipenv```-managed virtual environment and install the latest version of the package
```
pipenv install -i https://pypi.org/project/passwordManagerByAscii/0.2.2/
```
(Note that if you've previously created a pipenv virtual environment in the same directory, you may have to delete the old one first. Find out where it is located with the ```pipenv --venv``` command.)

2. Activate the virtual environment using this command
```
pipenv shell
```

3. Create a Python program file that imports the package and uses it. Check the [functions](#functions) section to see implementation in program.

4. Run the program using this command 
```
python3 my_program_filename.py
```

5. Exit the virtual environment with the command 
```
exit
```

## How to test package
1. Set up virtual enviroment following steps [number 1](#How-to-Install-and-use-the-Package)

2. Activate the virtual enviroment
```
pipenv shell
```
3. Install required packages to test and build the package
```
pipenv install pytest
pipenv install build
```
4. Build the package
```
python -m build
```
5. Test the package from main directory!
```
python3 -m pytest
```
6. Exit the virtual environment with the command 
```
exit
```

## Example program
Example application: [a password management program](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-11/blob/main/src/test.py)

The example application prompts the user to choose one of the five options by entering a number from 1 - 5: 
1. Generate Password: which prompts the user to enter a length between 6 to 15 characters. If the length was less than 6 characters or greater than 15 characters, the `generate_password` function will randomly generate a password in the range of 6 to 15. The generated password will be printed.

2. Encrypt Password: which prompts the user to input a password which will be encrypted using the `encode_password` function. Both the password provided by the user and the encrypted password will be printed.

3. Decrypt Password: which prompts the user to input a password which will be decrypted using the `decode_password`. Both the password provided by the user and the decrypted password will be printed.

4. Validate password: which prompts the user to enter a password which will be passed to the `validate_password` function. A message stating whether the password is valid or not will be printed.

5. Exit program: which will end the program. 

The program will keep prompting the user to choose an option unless the user enters the integer 5 which will end the program. Any input less than 1 or greater than 5 when choosing an option will result in an error message being printed and prompting the user to try again.

To access, click on the following link [a password management program](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-11/blob/main/src/test.py)

To run the program, follow the instructions found above under the `How to Install and use the Package` section.


