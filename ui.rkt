#lang racket/gui

(require racket/class
         gridcode/events)

(provide create-ui)

(define (create-ui runtime)
  (define size ((hash-ref runtime 'size)))
  (define window-size 640)
  (define cell-size (quotient window-size size))
  (define padding 1)
  (define inspection-enabled (box #f))
  (define inspected-cell (box #f))

  ((hash-ref runtime 'setup))

  ;; Main frame
  (define frame
    (new (class frame%
           (super-new)
           (define/augment (on-close)
             ((hash-ref runtime 'stop))))
         [label "GridCode"]
         [width window-size]
         [height (+ window-size 50)]))

  ;; Canvas with mouse handling
  (define canvas
    (new (class canvas%
           (super-new)
           (define/override (on-event event)
             (when (send event button-down?)
               (define x (quotient (send event get-x) cell-size))
               (define y (quotient (send event get-y) cell-size))
               (when (and (< x size) (< y size) (>= x 0) (>= y 0))
                 (if (unbox inspection-enabled)
                     (begin
                       (set-box! inspected-cell (list x y))
                       ((hash-ref runtime 'inspect-cell) x y))
                     ((hash-ref runtime 'cell-tapped) x y))
                 (send this refresh)))))
         [parent frame]
         [min-width window-size]
         [min-height window-size]
         [style '(border)]
         [paint-callback
          (lambda (canvas dc)
            (define t0 (current-inexact-milliseconds))

            ;; Black background
            (send dc set-brush "black" 'solid)
            (send dc draw-rectangle 0 0 window-size window-size)

            ;; Draw cells
            (for* ([x (in-range size)]
                   [y (in-range size)])
              (define color-vec ((hash-ref runtime 'color) x y))
              (define r (vector-ref color-vec 0))
              (define g (vector-ref color-vec 1))
              (define b (vector-ref color-vec 2))
              (define a (vector-ref color-vec 3))
              (define color (make-object color%
                              (exact-floor (* r 255))
                              (exact-floor (* g 255))
                              (exact-floor (* b 255))
                              a))
              (send dc set-brush color 'solid)
              (send dc draw-rectangle
                    (* x cell-size)
                    (* y cell-size)
                    (- cell-size padding)
                    (- cell-size padding)))

            ;; Inspection highlight
            (define coords (unbox inspected-cell))
            (when (and coords (list? coords))
              (define ix (first coords))
              (define iy (second coords))
              (define old-pen (send dc get-pen))
              (send dc set-pen "red" 2 'solid)
              (send dc set-brush "red" 'transparent)
              (send dc draw-rectangle
                    (* ix cell-size)
                    (* iy cell-size)
                    cell-size
                    cell-size)
              (send dc set-pen old-pen))

            ;; Print timing
            #;(define elapsed (- (current-inexact-milliseconds) t0))
            #;(displayln (format "~a Paint: ~a ms"
                                 t0
                                 (~r elapsed #:precision 2)))
            )]))

  ;; Button panel
  (define button-panel (new horizontal-panel%
                            [parent frame]
                            [alignment '(center center)]))

  (define restart-btn (new button%
                           [parent button-panel]
                           [label "Setup"]
                           [callback (lambda (b e) ((hash-ref runtime 'setup)))]))

  (define run-btn (new button%
                       [parent button-panel]
                       [label "Run"]
                       [callback (lambda (b e) ((hash-ref runtime 'start)))]))

  (define step-btn (new button%
                        [parent button-panel]
                        [label "Step"]
                        [callback (lambda (b e) ((hash-ref runtime 'update)))]))

  (define pause-btn (new button%
                         [parent button-panel]
                         [label "Stop"]
                         [callback (lambda (b e) ((hash-ref runtime 'stop)))]))

  (define inspect-btn (new check-box%
                           [parent button-panel]
                           [label "Inspect"]
                           [callback (lambda (b e)
                                       (set-box! inspection-enabled (send b get-value))
                                       (unless (unbox inspection-enabled)
                                         (set-box! inspected-cell #f)
                                         ((hash-ref runtime 'clear-inspection)))
                                       (send canvas refresh))]))

  ;; Repaint function
  (define (repaint)
    (send canvas refresh))

  ;; Event handlers
  (on 'grid-updated repaint)

  (on 'runtime-running
      (lambda (running)
        (send run-btn enable (not running))
        (send step-btn enable (not running))
        (send pause-btn enable running)))

  ;; Show frame
  (send frame show #t)

  ;; Return UI interface
  (hash 'repaint repaint
        'frame frame))