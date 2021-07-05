" dict.vim

if !has('python3')
    echo "Error: Vim must be compiled with +python3"
    finish
endif


function! ScratchBuf()
below new
setlocal nobuflisted buftype=nofile bufhidden=wipe noswapfile
return bufnr('%')
endfunction


function! Dict()

let mainbuf = bufnr('%')
let linebuf = getcurpos()
let scratchb = ScratchBuf()

python3 << EOF

import sys
import vim
import dict_py

scratchbuf = vim.eval('scratchb')
mainbuf = vim.eval('mainbuf')
linebuf = vim.eval('linebuf')

def dicto():
    dict_py.eval_txt(vim.buffers[int(mainbuf)], int(linebuf[1]), vim.buffers[int(scratchbuf)])

dicto()
EOF

endfunction


com! Dict call Dict()
nnoremap <C-k> :Dict<CR>


        
        

        

