# columnarTransposition
## Columnar Transposition cipher in Python


### Objective:
  
  Create a UI for Columnar Transposition Cipher using Python, Tkinter, using 256 characters and modificable shift for different results
  This is a transposition cipher which uses matrices to encrypt the data from a string received.
  
### UI: 
  
  Tkinter from Python
  - Two sections. One section to encrypt and decrypt using a keyword, another to only decrypt using a keyword.
  - Clean button.
  - Shift field changed to Keyword field.
  
### Cipher:

  Simple string methods and basic matrices operations to move the characters based on a keyword provided within the UI.
  The characters will not change but will be moved from their original position, and can only be decrypted if you have the keyword (while, in Caesar and Vigenere cipher, you could decrypt the string changing the offset until you find the right answer).
  
### Methods:

  - Cifrar() - Encrypt the string according to the shift indicated.
  - Descifrar() - Only the inverse of encrypt function, using the same shift specified before.
  
