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