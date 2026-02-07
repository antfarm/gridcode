#lang racket

(require gridcode/runtime 
         gridcode/ui)

(provide run)

(define (run prog)
  (define runtime (create-runtime prog))
  (define ui (create-ui runtime))
  (void))