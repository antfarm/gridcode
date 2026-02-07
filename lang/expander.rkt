#lang racket/base

(require racket
         gridcode/grid/main
         (for-syntax racket/base
                     racket/syntax))

(provide (all-from-out racket)
         (all-from-out gridcode/grid/main)
         program)

(define-syntax (program stx)
  (syntax-case stx ()
    [(_ name body ...)
     (let ([required '(grid-size frame-rate 
                       setup-grid update-grid 
                       color-for-cell info-for-cell 
                       handle-cell-tapped)]
           [defined '()])
       
       ;; Collect all definitions
       (for ([form (syntax->list #'(body ...))])
         (syntax-case form (define)
           [(define name _)
            (identifier? #'name)
            (set! defined (cons (syntax->datum #'name) defined))]
           [(define (name . _) . _)
            (identifier? #'name)
            (set! defined (cons (syntax->datum #'name) defined))]
           [_ (void)]))
       
       ;; Check for missing required names
       (for ([req required])
         (unless (member req defined)
           (raise-syntax-error 'program 
                               (format "Missing required definition: ~a" req)
                               stx)))
       
       ;; Generate the code
       (with-syntax ([grid-size-id (datum->syntax stx 'grid-size)]
                     [frame-rate-id (datum->syntax stx 'frame-rate)]
                     [setup-grid-id (datum->syntax stx 'setup-grid)]
                     [update-grid-id (datum->syntax stx 'update-grid)]
                     [color-for-cell-id (datum->syntax stx 'color-for-cell)]
                     [info-for-cell-id (datum->syntax stx 'info-for-cell)]
                     [handle-cell-tapped-id (datum->syntax stx 'handle-cell-tapped)])
         #'(begin
             body ...
             
             (define program
               (hash 'display-name name
                     'grid-size grid-size-id
                     'frame-rate frame-rate-id
                     'setup-grid setup-grid-id
                     'update-grid update-grid-id
                     'color-for-cell color-for-cell-id
                     'info-for-cell info-for-cell-id
                     'handle-cell-tapped handle-cell-tapped-id))
             
             (provide program))))]))