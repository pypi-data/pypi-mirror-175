![Python build & test](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-11/actions/workflows/build.yaml/badge.svg)

# passwordManagerByAscii Package
A pacakge that can generate, validate, encode, and decode passwords. built with build using setuptools, uploaded to PyPI using twine, and distributed via pip.

Checkout our package [at pypi](https://pypi.org/project/passwordManagerByAscii/0.2.2/)

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
- When users generate a password, it checks if the password is at least 6 characters, contains at least 1 special character, and at least 1 capital alphabet to maintain security. 
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
## Project Contribution
1. Install pipenv using the command 
```
python3 -m pip install --user pipenv
```
2. Activate the virtual enviroment
```
pipenv shell
```
3. Install required packages
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