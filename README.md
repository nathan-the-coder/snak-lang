## Mince Programming Language  


### Examples

Here is a example of a mince script

```mc 
use "std"
// define the main function
define hello(x, y) { 
    echo "This is the parent function\n"
    echo x, "\n"
    echo "This is y: ", y, "\n"
}

define loop() {
  x = 3
  echo x, "\n"
}

call hello(x:"Hello world", y:1)
call loop()
```


### FILES & DIRECTORIES
- the directory [editor](./editor) is where the all editor support will be stored.
- the directory [examples](./examples) is where all examples are stored.
- the directory [mcs](./mcs) or I call it 'mince extensions' will soon contain extensions for mince.

### INSTALLATION
##### For linux users
- cp the [mince.vim](./editor/vim/mince.vim) file (if you use neo/vim) to, ~/.vim/sytax or ~/.config/nvim/syntax/
- append the line that is on [filetype.vim](./editor/vim/filetype.vim) to neo/vim runtime directories
- run ./make install to install mince to ~/.local/bin.
##### For Windows
- you can just run the file using command prompt.


### NEW
- added [sedit](https://github.com/nathan-the-coder/sedit),
- it is the editor i've made specifically for my language.
- added file read and write function
- added support for running shell commands using the 'system' keyword 
- added simple error reporting using the error keyword 

### Notes
- Currently I wasn't able to implement function parameters,
- because its hard to code :).
- the keyword 'read' does not work properly
- but the write keyword works well :) 
