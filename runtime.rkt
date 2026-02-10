#lang racket

(require racket/class
         racket/gui/base
         gridcode/grid/main
         gridcode/events)

(provide create-runtime)

(define (create-runtime prog)

  (define display-name (hash-ref prog 'display-name))
  (define grid-size (hash-ref prog 'grid-size))
  (define frame-rate (hash-ref prog 'frame-rate))

  (define (setup-grid)
    (when timer
      (send timer stop))
    (init! grid-size)
    ((hash-ref prog 'setup-grid))
    (emit 'grid-updated)
    (print-inspected-cell)
    (when (unbox running?)
      (start-loop)))

  (define (update-grid)
    #;(define start (current-inexact-milliseconds))
    ((hash-ref prog 'update-grid))
    #;(define elapsed (- (current-inexact-milliseconds) start))
    #;(displayln (format "~a: update=~a (~a fps)"
                         start
                         (~r elapsed #:precision 2)
                         (~r (/ 1000.0 elapsed) #:precision 1)))
    (emit 'grid-updated)
    (print-inspected-cell)
    (yield))

  (define (color-for-cell x y)
    ((hash-ref prog 'color-for-cell) x y))

  (define (handle-cell-tapped x y)
    ((hash-ref prog 'handle-cell-tapped) x y))

  (define (handle-key-pressed key)
    ((hash-ref prog 'handle-key-pressed) key))

  ;; Run Loop

  (define timer #f)
  (define running? (box #f))

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

  ;; Cell Inspection

  (define inspected-cell (box #f))

  (define (inspect-cell x y)
    (set-box! inspected-cell (list x y))
    (print-inspected-cell))

  (define (clear-inspection)
    (set-box! inspected-cell #f))

  (define (print-inspected-cell)
    (when (unbox inspected-cell)
      (define coords (unbox inspected-cell))
      (displayln ((hash-ref prog 'info-for-cell) (first coords) (second coords))))
    )

  ;; Public Interface

  (hash 'display-name display-name
        'grid-size grid-size
        'frame-rate frame-rate
        'setup-grid setup-grid
        'update-grid update-grid
        'color-for-cell color-for-cell
        'handle-cell-tapped handle-cell-tapped
        'handle-key-pressed handle-key-pressed

        'start-loop start-loop
        'stop-loop stop-loop
        'running? running?
        'inspect-cell inspect-cell
        'clear-inspection clear-inspection))