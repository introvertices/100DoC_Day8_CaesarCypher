

def main():
  print(banner())
  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()


  # Get user's menu choice and validate all following inputs
  valid_menu_choice = False
  while not valid_menu_choice:
    try:
      if direction == "encode" or direction == "decode":
        valid_menu_choice = True
        text = input("\nType or paste your message:\n").lower()

        #Get the shift amount and fix it if it's over the typical alphabetical range
        shift = int(input("\nType a shift number:\n"))
        if shift > 26 or shift < 0:
          shift = shift_fix(shift)

        # Encode or decode depending on what was chosen  
        if direction == "encode":
          encrypt(text,shift)
        else:
          decrypt(text,shift)
        
      else:
        print("Invalid choice")
        direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    
    except ValueError:
      print("\nProgram failure: Shift must be a whole number")
    except:
      print("\nProgram failure, exiting.")


def banner():
  return '''
   _____                              _____ _       _               
  / ____|                            / ____(_)     | |              
 | |     __ _  ___  ___  __ _ _ __  | |     _ _ __ | |__   ___ _ __ 
 | |    / _` |/ _ \/ __|/ _` | '__| | |    | | '_ \| '_ \ / _ \ '__|
 | |___| (_| |  __/\__ \ (_| | |    | |____| | |_) | | | |  __/ |   
  \_____\__,_|\___||___/\__,_|_|     \_____|_| .__/|_| |_|\___|_|   
                                             | |                    
                                             |_|                    
  '''

def shift_fix(shift):
  return shift % 26


def encrypt(text,shift):
    cipher_text = []

    for i in text:
      # Gets the ASCII num value of the character in the passed text
      shifted_letter = ord(i) + shift
      # DEBUG - print(shifted_letter)

      # Will check if the current character is a letter, if it's not it skips shifting it.
      if i.isalpha():
        #Wrap around code to deal with letters being shifted past Z
        if shifted_letter > ord('z'):
          shifted_letter = shifted_letter - (ord('z') + 1 - ord('a'))
        cipher_text.append(chr(shifted_letter))
      else:
        cipher_text.append(i)
    
    print("".join(cipher_text))

def decrypt(text,shift):

    decrypted_text = []

    for i in text:
      # Will check if the current character is a letter, if it's not it skips shifting it. 
      if i.isalpha():
        # We shift INSIDE the if in decrypt mode so we don't screw up intentional punctuation
        shifted_letter = ord(i) - shift
        if shifted_letter < ord('a'):
          shifted_letter = (shifted_letter + 26)
      else:
        # Makes sure to keep the punctuation intact if it was not shifted
        shifted_letter = ord(i)
      decrypted_text.append(chr(shifted_letter))

    print("".join(decrypted_text))



if __name__ == "__main__":
  main()