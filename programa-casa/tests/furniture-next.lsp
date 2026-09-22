;;; CASA BH furniture 0.3. Prototype dimensions in mm; no regulatory claim.
(defun cf:rect (x y w h) (list x y (+ x w) (+ y h)))
(defun cf:hit (a b) (and (< (car a) (- (nth 2 b) 0.1)) (> (nth 2 a) (+ (car b) 0.1)) (< (cadr a) (- (nth 3 b) 0.1)) (> (nth 3 a) (+ (cadr b) 0.1))))
(defun cf:inside (a b) (and (>= (car a) (- (car b) 0.1)) (>= (cadr a) (- (cadr b) 0.1)) (<= (nth 2 a) (+ (nth 2 b) 0.1)) (<= (nth 3 a) (+ (nth 3 b) 0.1))))
(defun cf:item (kind box height use) (list (cons "kind" kind) (cons "bounds" box) (cons "height" height) (cons "use_bounds" (if use use box))))
(defun cf:template (kind w h double / out bx by bw seats tl cols dx)
  (setq out nil)
  (cond
    ((= kind "bedroom")
      (setq bw (if double 1380.0 880.0) bx (/ (- w bw) 2.0) by (- h 1980))
      (setq out (list
        (cf:item (if double "bed_double" "bed_single") (cf:rect bx by bw 1880) 550 (list (- bx 500) (- by 500) (+ bx bw 500) (- h 100)))
        (cf:item "wardrobe" (cf:rect 100 100 1500 600) 2200 (cf:rect 100 100 1500 1100))
        (cf:item "nightstand" (cf:rect (- bx 450) (- h 550) 400 450) 550 nil))))
    ((= kind "living")
      (setq seats (if *cf-occupants* *cf-occupants* 4))
      (if (<= seats 3)
        (setq out (list
          (cf:item "sofa" (cf:rect (/ (- w 2200) 2.0) (- h 1000) 2200 900) 850 (cf:rect (/ (- w 2200) 2.0) (- h 1600) 2200 1500))
          (cf:item "tv_rack" (cf:rect (/ (- w 1500) 2.0) 100 1500 350) 550 (cf:rect (/ (- w 1500) 2.0) 100 1500 950))))
        (setq out (list
          (cf:item "sofa" (cf:rect (/ (- w 2200) 2.0) (- h 1000) 2200 900) 850 (cf:rect (/ (- w 2200) 2.0) (- h 1600) 2200 1500))
          (cf:item "sofa" (cf:rect (/ (- w 2200) 2.0) 100 2200 900) 850 (cf:rect (/ (- w 2200) 2.0) 100 2200 1500))
          (cf:item "tv_rack" (cf:rect 50 (/ (- h 1000) 2.0) 300 1000) 550 (cf:rect 50 (/ (- h 1000) 2.0) 900 1000)))))
      (if (= seats 4)
        (setq out (list
          (cf:item "sofa" (cf:rect (/ (- w 2200) 2.0) (- h 1000) 2200 900) 850 (cf:rect (/ (- w 2200) 2.0) (- h 1600) 2200 1500))
          (cf:item "armchair" (cf:rect 100 100 750 750) 850 (cf:rect 100 100 750 1350))
          (cf:item "tv_rack" (cf:rect (- w 350) 1400 300 1000) 550 (cf:rect (- w 950) 1400 900 1000)))))
      (if (and (>= seats 5) *cf-variant* (= *cf-variant* 1))
        (progn
          (setq out (list
            (cf:item "sofa" (cf:rect (/ (- w 2200) 2.0) (- h 1000) 2200 900) 850 (cf:rect (/ (- w 2200) 2.0) (- h 1600) 2200 1500))
            (cf:item "loveseat" (cf:rect 100 100 800 1600) 850 (cf:rect 100 100 1400 1600))
            (cf:item "tv_rack" (cf:rect (- w 350) 1400 300 1000) 550 (cf:rect (- w 950) 1400 900 1000))))
          (if (= seats 6) (setq out (append out (list
            (cf:item "armchair" (cf:rect (- w 850) 100 750 750) 850 (cf:rect (- w 850) 100 750 1250))))))))      (if (> seats 6) (setq out nil)))
    ((= kind "dining")
      (setq seats (if *cf-occupants* *cf-occupants* 4) cols (cond ((<= seats 4) 2) ((<= seats 6) 3) (T 4)) tl (cond ((= cols 2) 1400) ((= cols 3) 1800) (T 2300)) bx (/ (- w tl) 2.0) by (/ (- h 800) 2.0))
      (setq out (list (cf:item "dining_table" (cf:rect bx by tl 800) 750 nil)) dx 100)
      (repeat cols
        (setq out (append out (list
          (cf:item "dining_chair" (cf:rect (+ bx dx) (- by 450) 450 400) 850 (cf:rect (+ bx dx) (- by 850) 450 800))
          (cf:item "dining_chair" (cf:rect (+ bx dx) (+ by 850) 450 400) 850 (cf:rect (+ bx dx) (+ by 850) 450 800)))))
        (setq dx (+ dx 550))))
    ((= kind "kitchen")
      (setq out (list
        (cf:item "fridge" (cf:rect 100 (- h 850) 700 750) 1800 (cf:rect 100 (- h 1600) 700 1500))
        (cf:item "sink" (cf:rect 850 (- h 700) 600 600) 900 (cf:rect 850 (- h 1500) 600 1400))
        (cf:item "counter" (cf:rect 1450 (- h 700) 400 600) 900 (cf:rect 1450 (- h 1500) 400 1400))
        (cf:item "stove" (cf:rect 1900 (- h 700) 600 600) 900 (cf:rect 1900 (- h 1500) 600 1400)))))
    ((= kind "bathroom")
      (setq out (list
        (cf:item "shower" (cf:rect 100 (- h 1000) 900 900) 100 (cf:rect 100 (- h 1500) 900 1400))
        (cf:item "toilet" (cf:rect 1100 (- h 850) 650 750) 700 (cf:rect 1100 (- h 1450) 650 1350))
        (cf:item "basin" (cf:rect (- w 650) 100 550 450) 850 (cf:rect (- w 1250) 100 1150 450)))))
    ((= kind "laundry")
      (setq out (list
        (cf:item "washer" (cf:rect 100 (- h 800) 650 700) 900 (cf:rect 100 (- h 1500) 650 1400))
        (cf:item "laundry_sink" (cf:rect 850 (- h 700) 600 600) 900 (cf:rect 850 (- h 1500) 600 1400)))))
    ((= kind "office")
      (setq bx (/ (- w 1200) 2.0))
      (setq out (list
        (cf:item "desk" (cf:rect bx (- h 700) 1200 600) 750 nil)
        (cf:item "office_chair" (cf:rect (+ bx 350) (- h 1300) 500 500) 950 (cf:rect (+ bx 250) (- h 1700) 700 900)))))
    ((= kind "garage")
      (setq cols (if *cf-garage-spaces* *cf-garage-spaces* 1) dx 0 bw (/ w cols))
      (repeat cols
        (setq out (append out (list (cf:item "car" (cf:rect (+ dx (/ (- bw 1800) 2.0)) (/ (- h 4400) 2.0) 1800 4400) 1500 (cf:rect (+ dx (/ (- bw 2600) 2.0)) (/ (- h 4800) 2.0) 2600 4800)))))
        (setq dx (+ dx bw))))    ((member kind '("veranda" "terrace"))
      (setq out (list (cf:item "bench" (cf:rect 100 (- h 550) 1500 450) 800 (cf:rect 100 (- h 1150) 1500 1050)))))
  ) out)
(defun cf:pt (p w h rot mirror / x y)
  (setq x (car p) y (cadr p))
  (if mirror (setq x (- w x)))
  (cond ((= rot 0) (list x y)) ((= rot 1) (list (- h y) x)) ((= rot 2) (list (- w x) (- h y))) (T (list y (- w x)))))
(defun cf:transform (b box w h rot mirror / a c)
  (setq a (cf:pt (list (car b) (cadr b)) w h rot mirror) c (cf:pt (list (nth 2 b) (nth 3 b)) w h rot mirror))
  (list (+ (car box) (min (car a) (car c))) (+ (cadr box) (min (cadr a) (cadr c))) (+ (car box) (max (car a) (car c))) (+ (cadr box) (max (cadr a) (cadr c)))))
(defun cf:doors (box model / out op c wd depth x y ds)
  (setq out nil)
  (foreach op (cg:get "openings" model)
    (if (= (cg:get "kind" op) "door")
      (progn
        (setq c (cg:get "center" op) wd (+ (/ (cg:get "width" op) 2.0) 50) x (car c) y (cadr c)
          ds (cg:opt "door_style" op "swing") depth (if (member ds '("passage" "sliding")) 450 (+ (cg:get "width" op) 100)))
        (cond
          ((and (<= (abs (- x (car box))) 350) (> y (cadr box)) (< y (nth 3 box))) (setq out (cons (list (car box) (- y wd) (+ (car box) depth) (+ y wd)) out)))
          ((and (<= (abs (- x (nth 2 box))) 350) (> y (cadr box)) (< y (nth 3 box))) (setq out (cons (list (- (nth 2 box) depth) (- y wd) (nth 2 box) (+ y wd)) out)))
          ((and (<= (abs (- y (cadr box))) 350) (> x (car box)) (< x (nth 2 box))) (setq out (cons (list (- x wd) (cadr box) (+ x wd) (+ (cadr box) depth)) out)))
          ((and (<= (abs (- y (nth 3 box))) 350) (> x (car box)) (< x (nth 2 box))) (setq out (cons (list (- x wd) (- (nth 3 box) depth) (+ x wd) (nth 3 box)) out))))))) out)
(defun cf:valid (items box doors / ok a b d)
  (setq ok T)
  (foreach a items
    (if (not (and (cf:inside (cg:get "bounds" a) box) (cf:inside (cg:get "use_bounds" a) box))) (setq ok nil))
    (foreach b items (if (and (not (eq a b)) (or (cf:hit (cg:get "bounds" a) (cg:get "bounds" b)) (and (not (and (member (cg:get "kind" a) '("bed_double" "bed_single")) (= (cg:get "kind" b) "nightstand"))) (cf:hit (cg:get "use_bounds" a) (cg:get "bounds" b))))) (setq ok nil)))
    (foreach d doors (if (cf:hit (cg:get "bounds" a) d) (setq ok nil)))) ok)
(defun cf:window-clear (items model / ok it op wall a b c half band candidate)
  (setq ok T)
  (foreach op (cg:get "openings" model)
    (if (= (cg:get "kind" op) "window")
      (progn
        (setq wall nil)
        (foreach candidate (cg:get "walls" model) (if (= (cg:get "id" candidate) (cg:get "wall_id" op)) (setq wall candidate)))
        (if wall
          (progn
            (setq a (cg:get "start" wall) b (cg:get "end" wall) c (cg:get "center" op) half (/ (cg:get "width" op) 2.0))
            (if (equal (car a) (car b) 0.1)
              (setq band (list (- (car c) (+ 200 (/ (cg:get "thickness" wall) 2.0))) (- (cadr c) half) (+ (car c) (+ 200 (/ (cg:get "thickness" wall) 2.0))) (+ (cadr c) half)))
              (setq band (list (- (car c) half) (- (cadr c) (+ 200 (/ (cg:get "thickness" wall) 2.0))) (+ (car c) half) (+ (cadr c) (+ 200 (/ (cg:get "thickness" wall) 2.0))))))
            (foreach it items
              (if (and (> (cg:get "height" it) (cg:opt "sill" op 900)) (cf:hit (cg:get "bounds" it) band)) (setq ok nil)))))))) ok)(defun cf:place (zone model double / box ww hh rot mir w h temp items it doors found attempt *cf-variant*)
  (setq box (cg:get "bounds" zone) ww (- (nth 2 box) (car box)) hh (- (nth 3 box) (cadr box)) doors (cf:doors box model) found nil rot 0 attempt 0)
  (repeat 8
    (setq rot (rem attempt 4) *cf-variant* (fix (/ attempt 4)))
    (setq w (if (= (rem rot 2) 0) ww hh) h (if (= (rem rot 2) 0) hh ww))
    (foreach mir '(nil T)
      (if (not found)
        (progn
          (setq temp (cf:template (cg:get "kind" zone) w h double) items nil)
          (foreach it temp
            (setq items (append items (list (list
              (cons "kind" (cg:get "kind" it)) (cons "height" (cg:get "height" it))
              (cons "bounds" (cf:transform (cg:get "bounds" it) box w h rot mir))
              (cons "use_bounds" (cf:transform (cg:get "use_bounds" it) box w h rot mir))
              (cons "rotation" (* rot 90)) (cons "room_id" (cg:opt "room_id" zone (cg:get "id" zone))) (cons "zone_id" (cg:get "id" zone)))))))
          (if (and items (cf:valid items box doors) (cf:window-clear items model)) (setq found items)))))
    (setq attempt (1+ attempt))) found)
(defun cf:replace (key val model) (if (assoc key model) (subst (cons key val) (assoc key model) model) (append model (list (cons key val)))))
(defun cg:furnish-model (model params / zones zone items all err beds cap kind num vals result it *cf-occupants* *cf-garage-spaces* doubleCount)
  (setq *cf-occupants* (fix (cg:opt "occupants" params 4)) doubleCount (max 1 (- *cf-occupants* (fix (cg:opt "bedrooms" params 3)))))
  (setq zones (cg:opt "zones" model (cg:get "rooms" model)) all nil err nil beds 0 cap 0 num 0)
  (if (= (cg:opt "furniture" params 1) 1)
    (progn
      (foreach zone zones
        (setq kind (cg:get "kind" zone))
        (if (member kind '("bedroom" "living" "dining" "kitchen" "bathroom" "laundry" "office"))
          (progn
            (setq items (cf:place zone model (and (= kind "bedroom") (< beds doubleCount))))
            (if items (setq all (append all items)) (setq err (strcat "Conjunto funcional nao cabe: " (cg:opt "name" zone kind) ". Ajuste dimensoes ou tente outra alternativa.")))
            (if (= kind "bedroom") (setq cap (+ cap (if (< beds doubleCount) 2 1)) beds (1+ beds))))))
      (foreach zone (cg:get "outdoor" model)
        (if (member (cg:get "kind" zone) '("garage" "veranda" "terrace"))
          (progn (setq *cf-garage-spaces* (fix (cg:opt "spaces" zone 1)) items (cf:place zone model nil))
            (if items (setq all (append all items)) (setq err (strcat "Conjunto externo nao cabe: " (cg:get "kind" zone)))))))
      (if (< cap *cf-occupants*) (setq err "Quantidade de camas insuficiente para moradores. Perfil suporta ate duas pessoas por quarto."))
      (if (> *cf-occupants* 6) (setq err "Perfil de mobiliario atual suporta ate 6 moradores; reduza moradores ou amplie o catalogo de conviv?ncia."))
      (setq result nil)
      (foreach it all (setq num (1+ num) result (append result (list (cons (cons "id" (strcat "F" (itoa num))) it)))))
      (setq vals (append (cg:get "validations" model) (list
        (list (cons "rule_id" "FURNITURE_CLEARANCE") (cons "status" (if err "fail" "pass")) (cons "message" "Limites, sobreposicao, faixas de uso de catalogo, reservas nas portas e pecas altas junto a janelas; nao equivale a acessibilidade."))
        (list (cons "rule_id" "SLEEPING_CAPACITY") (cons "status" (if (>= cap (cg:opt "occupants" params 4)) "pass" "warning")) (cons "message" (strcat "Capacidade de camas: " (itoa cap) ". Moradores informados: " (itoa (fix (cg:opt "occupants" params 4)))))))))
      (if err (list (cons "error" err)) (cf:replace "validations" vals (cf:replace "furniture" result model))))
    (cf:replace "furniture" nil model)))
(princ)











