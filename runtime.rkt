#lang racket

(require racket/class
         racket/gui/base
         gridcode/grid/main 
         gridcode/events)

(provide create-runtime)

(define (create-runtime prog)
  (define size (hash-ref prog 'grid-size))
  (define frame-rate (hash-ref prog 'frame-rate))
  (define running? (box #f))
  (define timer #f)
  (define inspected-cell (box #f))

  (define (setup-grid)
    (when timer
      (send timer stop))
    (init! size)
    ((hash-ref prog 'setup-grid))
    (emit 'grid-updated)
    (when (unbox running?)
      (start-loop)))

  (define (update-grid)
    (define start (current-inexact-milliseconds))
    ((hash-ref prog 'update-grid))
    (define elapsed (- (current-inexact-milliseconds) start))
    #;(displayln (format "~a: update=~a (~a fps)"
                         start
                         (~r elapsed #:precision 2)
                         (~r (/ 1000.0 elapsed) #:precision 1)))
    (emit 'grid-updated)
    ;; Print inspected cell info if one is selected
    (when (unbox inspected-cell)
      (define coords (unbox inspected-cell))
      (displayln ((hash-ref prog 'info-for-cell) (first coords) (second coords))))
    (yield))

  (define (start-loop)
    (set-box! running? #t)
    (emit 'runtime-running #t)
    (update-grid)
    (define interval-ms (inexact->exact (floor (/ 1000.0 frame-rate))))
    (set! timer (new timer%
                     [notify-callback update-grid]
                     [interval interval-ms]
                     [just-once? #f]))
    (send timer start interval-ms))

  (define (stop-loop)
    (set-box! running? #f)
    (emit 'runtime-running #f)
    (when timer
      (send timer stop)))

  ;; Event handlers
  (on 'restart-requested setup-grid)
  (on 'run-requested start-loop)
  (on 'step-requested update-grid)
  (on 'pause-requested stop-loop)

  (on 'cell-inspected
      (lambda (coords)
        (set-box! inspected-cell coords)
        (when coords
          (displayln ((hash-ref prog 'info-for-cell) (first coords) (second coords))))))

  ;; Return runtime interface
  (hash 'setup setup-grid
        'update update-grid
        'start start-loop
        'stop stop-loop
        'running? running?))