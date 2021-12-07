

def main():
  print(banner())

  direction = input("\033[1;32;40mType 'encode' to encrypt, type 'decode' to decrypt, or crack to crack a code:\033[1;37;40m\n").lower()

  # Get user's menu choice and validate all following inputs
  valid_menu_choice = False
  while not valid_menu_choice:
    try:
      if direction == "encode" or direction == "decode":

        # Grabs the user's text input. Can include punctuation.
        text = input("\n\033[1;32;40mType or paste your message:\033[1;37;40m\n").lower()

        #Get the shift amount and fix it if it's over the typical alphabetical range
        shift = int(input("\n\033[1;32;40mType a shift number:\033[1;37;40m\n"))
        if shift > 26 or shift < 0:
          shift = shift_fix(shift) # Accounts for wrap around of letters

        #Toggle the menu loop off since both previous inputs were valid.
        valid_menu_choice = True

        # Encode or decode depending on what was chosen  
        if direction == "encode":
          encrypt(text,shift)
        else:
          decrypt(text,shift, True) #Runs with print out intact

      elif direction == "crack":
        valid_menu_choice = True
        text = input("\n\033[1;32;40mType or paste your message ONLY THE FIRST 20 CHARS WILL BE SHIFTED FOR PREVIEW PURPOSES!:\033[1;37;40m\n").lower()
        crack(text)
        
      else:
        print("\033[1;31;40mInvalid choice")
        direction = input("\033[1;32;40mType 'encode' to encrypt, type 'decode' to decrypt, or crack to crack a code:\033[1;37;40m\n")
    
    except ValueError:
      print("\n\033[1;31;40mShift must be a whole number, try again")
    except:
      print("\n\033[1;31;40mProgram failure, exiting.")



#!-- FUNCTIONS

####### ASCII banner
def banner():
  return '''\033[1;32;40m
 ██████╗ █████╗ ███████╗███████╗ █████╗ ██████╗        ██╗       ██████╗ ██████╗ ██╗   ██╗████████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗       ██║       ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██║   ██║██╔════╝
██║     ███████║█████╗  ███████╗███████║██████╔╝    ████████╗    ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║███████╗
██║     ██╔══██║██╔══╝  ╚════██║██╔══██║██╔══██╗    ██╔═██╔═╝    ██╔══██╗██╔══██╗██║   ██║   ██║   ██║   ██║╚════██║
╚██████╗██║  ██║███████╗███████║██║  ██║██║  ██║    ██████║      ██████╔╝██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝
  \033[1;33;40m                                                                                                      
  MENU:
  ---------------------------
  1. Encrypt                |
  2. Decrypt                |-----> Pick a choice and your .txt file will be created
  3. Crack (20 Char Preview)|                                                                                
  ---------------------------         
  '''


####### Required to fix any wrap around issues, maps remainder to the appropriate letter
def shift_fix(shift):
  return shift % 26


####### Encrypt user's text and prints out the result and also saves to a file
def encrypt(text,shift):
  cipher_text = []

  for i in text:
    # Gets the ASCII num value of the character in the passed text
    shifted_letter = ord(i) + shift

    # Will check if the current character is a letter, if it's not it skips shifting it.
    if i.isalpha():
      #Wrap around code to deal with letters being shifted past Z
      if shifted_letter > ord('z'):
        shifted_letter = shifted_letter - (ord('z') + 1 - ord('a'))
      cipher_text.append(chr(shifted_letter))
    else:
      cipher_text.append(i)
  
  print("".join(cipher_text))
  
  # Throw result into a file
  print(f"\n\033[1;37;40mEncrypting entry to encrypted.txt")
  with open("encrypted.txt",'a') as result_file:
    result_file.write(f"\n\nInput:\n{text}\n\nOutput:\n{''.join(cipher_text)}")
  print("\033[1;32;40mFile written successfully!")


####### Decrypt the user's inputted text and saves it to a file
def decrypt(text,shift,run_print):

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

  # Throw result into a file but only if this isn't a crack
  if run_print == True:
    print(f"\n\033[1;37;40mDecrypting entry to decrypted.txt")
    with open("decrypted.txt",'a') as result_file:
      result_file.write(f"\n\nInput:\n{text}\n\nOutput:\n{''.join(decrypted_text)}")
    print("\033[1;32;40mFile written successfully!")
    print("".join(decrypted_text))

  return "".join(decrypted_text)


####### Automatically goes through each shift to crack the code in an instance where a user might not know the shift (or is being lazy)
def crack(text):

  print("\n\033[1;37;40mPlease note only the first 20 characters will be cracked and the results are only a PREVIEW to discern the correct result! You will be shown the results along with the shift number, and may then select the correct shift - which will then write the whole text to CRACKED.TXT\n")
  shift_max = 26
  possible_results = []
  preview_text = ""

  # First grab the first 20 characters or the max length of the string
  if len(text) <= 20:
    preview_text = text
  else:
    for i in range(20):
      preview_text += text[i]

  # For each possible shift perform a decrypt, and add the result to possible_results
  for s in range(shift_max):
    decrypted_text = []
    for i in preview_text:
      # Will check if the current character is a letter, if it's not it skips shifting it. 
      if i.isalpha():
        # We shift INSIDE the if in decrypt mode so we don't screw up intentional punctuation
        shifted_letter = ord(i) - s
        if shifted_letter < ord('a'):
          shifted_letter = (shifted_letter + 26)
      else:
        # Makes sure to keep the punctuation intact if it was not shifted
        shifted_letter = ord(i)
      decrypted_text.append(chr(shifted_letter))

    possible_results.append("".join(decrypted_text))

  # Display the results to the user so they can write the result to a file if they wish
  print("\033[1;37;40mShift  | Result")
  for index,result in enumerate(possible_results):
    current_index = str(index)
    print(f"{current_index}{' '*(7-len(current_index))}| {result}")
  
  # Get the user to input the correct result, and write it to a file, unless they specify no or an incorrect number
  to_shift = input("\n\033[1;37;40mType the number of the correct entry to export, or type 'no' to exit: \n").lower()
  try:
    if int(to_shift) >0 or int(to_shift) <= 26:
      print(f"\n\033[1;37;40mDecrypting entry {to_shift} to CRACKED.txt")
      full_decode = decrypt(text,int(to_shift),False)
      with open("CRACKED.txt",'a') as result_file:
        result_file.write("\n\n")
        result_file.write(full_decode)
      print("\033[1;32;40mFile written successfully!")
  except:
    print("\033[1;37;40mExiting")

if __name__ == "__main__":
  main()