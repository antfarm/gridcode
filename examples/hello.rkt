#lang gridcode

(define my-program
  (hash 'grid-size 16
        'frame-rate 2

        'setup-grid (lambda ()
                      (for ([x (in-range 16)])
                        (set-cell! x x "alive" #t)))
        
        'update-grid (lambda ()
                       (for* ([x (in-range 16)]
                              [y (in-range 16)])
                         (define alive (get-cell x y "alive"))
                         (set-cell! x y "alive" (not alive))))
        
        'color-for-cell (lambda (x y)
                          (if (get-cell x y "alive")
                              (color 1.0 0.8 0.2)
                              (color 0.0 0.0 0.0)))
        
        'info-for-cell (lambda (x y)
                         (format "[~a|~a] alive: ~a" x y (get-cell x y "alive")))
        
        'handle-cell-tapped (lambda (x y)
                              (define alive (get-cell x y "alive"))
                              (set-cell! x y "alive" (not alive)))))

(void (run my-program))