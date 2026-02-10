#lang info

(define collection "gridcode")

(define deps '("base" "gui-lib"))

(define racket-launcher-names '("gridcode"))
(define racket-launcher-libraries '("gridcode.rkt"))

;; To re-install:
;;   raco pkg remove gridcode
;;   raco pkg install --link ../gridcode