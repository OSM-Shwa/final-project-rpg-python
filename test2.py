def file_handler_v1(command: str) -> None:
    match command.split():
        case ['show']:         
            print('List all files and directories: ')
            # code to list files
        case ['remove', *files]:
            print(f'Removing files: {files}')
            # code to remove files
        case _:
           print('Command not recognized.')

# file_handler_v1('remove file1.txt file2.jpg file3.pdf')

def file_handler_v2(command):
      match command.split():
          case ['show']:
              print('List all files and directories: ')
              # code to list files
          case ['remove' | 'delete', *files] if '--ask' in files:
              del_files = [f for f in files if len(f.split('.'))>1]
              print(f'Please confirm: Removing files: {del_files}')
              # code to accept user input, then remove files
          case ['remove' | 'delete', *files]:
              print(f'Removing files: {files}')
              # code to remove files
          case _:
              print('Command not recognized')
              
file_handler_v2('remove --ask file1.txt file2.jpg file3.pdf')