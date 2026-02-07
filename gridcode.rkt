#lang racket

(require gridcode/runtime 
         gridcode/ui)

(provide run)

(define (run prog)
  (define runtime (create-runtime prog))
  (define ui (create-ui runtime))
  (void))

(module+ main
  (define args (current-command-line-arguments))
  
  (when (< (vector-length args) 1)
    (displayln "Usage: racket gridcode.rkt <program-file>")
    (exit 1))
  
  (define filepath (vector-ref args 0))
  
  ;; Use dynamic-require to get the provided value directly
  (define prog (dynamic-require filepath 'program))
  
  (unless prog
    (displayln "Error: Program must define and provide 'program'")
    (exit 1))
  
  (run prog))