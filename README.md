# Mince Programming Language
A lua-like language that is written in Python and compiled using Cython

### Examples

```mince
defun main
  print "Hello from mince"

  i = "Hello"

  if i == "Hello" then
    print "Hello from mince"
  else
    print "Hello world"
  end
end

inv test
```


### FILES & DIRECTORIES
- [editor](./editor): for text editor support. 
- [examples](./examples): contains examples for you to test out

### INSTALLATION
##### For linux users
for neo/vim users just copy the [filetype.vim](./editor/vim/filetype.vim)
to '~/.config/nvim' for neovim or to '~/.vim' for vim.
and the syntax file [mc.vim](./editor/vim/mc.vim) to '~/.config/nvim/syntax' or '~/.vim/syntax'

```bash
$ mkdir -p ~/.config/nvim/syntax # for neovim
$ mkdir -p ~/.vim/syntax # for vim

$ cp ./editor/vim/mc.vim ~/.config/nvim/syntax # for neovim
$ cp ./editor/vim/mc.vim ~/.vim/syntax # for vim

$ cp ./editor/vim/filetype.vim ~/.config/nvim # for neovim
$ cp ./editor/vim/filetype.vim ~/.vim # for vim

```

to use mince you can compile it using:

```bash
$ sudo make install # it will install mince to /usr/local/bin
```

##### For Windows
if your on Windows, it does not need any installation 
just do the things below
P.S use windows powershell to run these commands.

```bash
> git clone https://github.com/nathan-the-coder/mince  # assuming you have git installed 
> cd mince
```

if you want to use just python then you can just do:

```bash
#to run the file you made just:
> .\mince.py # <your file>
# or
> python3 .\mince.py # <your file>
```

> you must have mingw-w64 installed with make to compile it
> if you want to compile it to machine code then just do:
```bash
# you must use windows powershell to be able to run these
make  
# to run it just 
.\mince # <your file>
```

PS. idk how to compile mince to windows, because I use linux to build it

if you use neo/vim just do the steps above on how to apply the filetype 
and syntax support, but change the '~/.config/nvim' to '%userprofile%\AppData\Local\nvim'
```bash
# you must use windows powershell to be able to run these
cp editor\vim\filetype.vim %userprofile%\AppData\Local\nvim

mkdir %userprofile%\AppData\Local\nvim\syntax

cp editor\vim\mc.vim %userprofile%\AppData\Local\nvim\syntax
```
> for vim change the '~/.vim' to '%userprofile%\AppData\Local\vim'
> P.S idk exactly the location of the user config of vim on Windows


### NEW
> I am still trying to figure out how to implement
> the incrementing and decrementing of a integer variable 

- It is now became a compiled language thanks to Cython.
- Changed the syntax similar with the lua syntax

### Notes

> for function there is no parameters,
> simply because I can't code it, 
> I am only the one who code and implement 
> all of the code.

- It is not a toy Language
- It is not turing complete.
- The development will continue
- It doesn't have some complex functionalities 
that other 'popular' language have.
