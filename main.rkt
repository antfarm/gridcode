#lang racket

(require gridcode/grid/main 
         gridcode/runtime 
         gridcode/ui)

(provide run)

(define (run prog)
  (init! (hash-ref prog 'grid-size))
  ((hash-ref prog 'setup-grid))

  (define ui (create-ui prog))
  (define runtime (create-runtime prog))

  (hash 'ui ui
        'runtime runtime))