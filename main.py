"""
Scratch Code — editor visual de bloques con dibujo de personajes y fondos.
Solo usa la librería estándar de Python 3.14 (tkinter, json, math, time, re,
threading, os). No requiere instalar nada.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
import json, math, time, re, threading, os

# ══════════════════════════════════════════════════════════════════
# 1. IDIOMAS
# ══════════════════════════════════════════════════════════════════
LANGS = ["es", "en", "pt", "fr", "ru", "ja"]
LANG_NAMES = {"es":"Español","en":"English","pt":"Português",
              "fr":"Français","ru":"Русский","ja":"日本語"}

T = {
 "es": {
  "file":"Archivo","new":"Nuevo","open":"Abrir","save":"Guardar","exit":"Salir",
  "lang":"Idioma","help":"Ayuda","palette":"Bloques","script":"Guion","stage":"Escenario",
  "run":"▶ Ejecutar","stop":"■ Detener","clear":"Limpiar",
  "sprites":"Personajes","backdrops":"Fondos",
  "add_sprite":"+ Personaje","add_backdrop":"+ Fondo",
  "edit":"Editar","upload":"Subir imagen","delete":"Eliminar",
  "cat_ev":"Eventos","cat_mo":"Movimiento","cat_lo":"Apariencia","cat_co":"Control",
  "cat_se":"Sensores","cat_op":"Operadores","cat_va":"Variables","cat_pe":"Lápiz",
  "saved":"Guardado:","loaded":"Cargado:","err":"Error",
  "newq":"¿Descartar el guion actual?","help_txt":
   "Cómo usar:\n\n"
   "1. Haz clic en los bloques de la izquierda para añadirlos.\n"
   "2. Usa Tab para indentar dentro de bloques C.\n"
   "3. Pulsa ▶ Ejecutar.\n\n"
   "Personajes y fondos:\n"
   "• '+ Personaje' añade un sprite.\n"
   "• 'Editar' abre el editor de píxeles.\n"
   "• 'Subir imagen' carga un GIF/PNG.\n"
   "• Lo mismo para fondos.\n\n"
   "Guarda con extensión .sc",
  # Editor
  "ed_title_sprite":"Editar personaje","ed_title_backdrop":"Editar fondo",
  "ed_color":"Color","ed_eraser":"Borrador","ed_fill":"Rellenar","ed_clear":"Limpiar",
  "ed_undo":"Deshacer","ed_save":"✓ Guardar","ed_cancel":"✗ Cancelar",
  "ed_palette":"Paleta rápida","ed_tools":"Herramientas",
  "choose_img":"Elegir imagen","pick_color":"Elegir color",
 },
 "en": {
  "file":"File","new":"New","open":"Open","save":"Save","exit":"Exit",
  "lang":"Language","help":"Help","palette":"Blocks","script":"Script","stage":"Stage",
  "run":"▶ Run","stop":"■ Stop","clear":"Clear",
  "sprites":"Sprites","backdrops":"Backdrops",
  "add_sprite":"+ Sprite","add_backdrop":"+ Backdrop",
  "edit":"Edit","upload":"Upload image","delete":"Delete",
  "cat_ev":"Events","cat_mo":"Motion","cat_lo":"Looks","cat_co":"Control",
  "cat_se":"Sensing","cat_op":"Operators","cat_va":"Variables","cat_pe":"Pen",
  "saved":"Saved:","loaded":"Loaded:","err":"Error",
  "newq":"Discard current script?","help_txt":
   "How to use:\n\n"
   "1. Click blocks on the left.\n"
   "2. Use Tab to indent inside C-blocks.\n"
   "3. Press ▶ Run.\n\n"
   "Sprites & backdrops:\n"
   "• '+ Sprite' adds a sprite.\n"
   "• 'Edit' opens the pixel editor.\n"
   "• 'Upload image' loads a GIF/PNG.\n"
   "• Same for backdrops.\n\n"
   "Save with .sc extension",
  "ed_title_sprite":"Edit sprite","ed_title_backdrop":"Edit backdrop",
  "ed_color":"Color","ed_eraser":"Eraser","ed_fill":"Fill","ed_clear":"Clear",
  "ed_undo":"Undo","ed_save":"✓ Save","ed_cancel":"✗ Cancel",
  "ed_palette":"Quick palette","ed_tools":"Tools",
  "choose_img":"Choose image","pick_color":"Pick color",
 },
 "pt": {
  "file":"Arquivo","new":"Novo","open":"Abrir","save":"Salvar","exit":"Sair",
  "lang":"Idioma","help":"Ajuda","palette":"Blocos","script":"Roteiro","stage":"Palco",
  "run":"▶ Executar","stop":"■ Parar","clear":"Limpar",
  "sprites":"Personagens","backdrops":"Cenários",
  "add_sprite":"+ Personagem","add_backdrop":"+ Cenário",
  "edit":"Editar","upload":"Enviar imagem","delete":"Excluir",
  "cat_ev":"Eventos","cat_mo":"Movimento","cat_lo":"Aparência","cat_co":"Controle",
  "cat_se":"Sensores","cat_op":"Operadores","cat_va":"Variáveis","cat_pe":"Caneta",
  "saved":"Salvo:","loaded":"Carregado:","err":"Erro",
  "newq":"Descartar o roteiro atual?","help_txt":
   "Como usar:\n\n"
   "1. Clique nos blocos à esquerda.\n"
   "2. Use Tab para indentar dentro de blocos C.\n"
   "3. Pressione ▶ Executar.\n\n"
   "Personagens e cenários:\n"
   "• '+ Personagem' adiciona um sprite.\n"
   "• 'Editar' abre o editor de pixels.\n"
   "• 'Enviar imagem' carrega GIF/PNG.\n"
   "• O mesmo para cenários.\n\n"
   "Salve com extensão .sc",
  "ed_title_sprite":"Editar personagem","ed_title_backdrop":"Editar cenário",
  "ed_color":"Cor","ed_eraser":"Borracha","ed_fill":"Preencher","ed_clear":"Limpar",
  "ed_undo":"Desfazer","ed_save":"✓ Salvar","ed_cancel":"✗ Cancelar",
  "ed_palette":"Paleta rápida","ed_tools":"Ferramentas",
  "choose_img":"Escolher imagem","pick_color":"Escolher cor",
 },
 "fr": {
  "file":"Fichier","new":"Nouveau","open":"Ouvrir","save":"Enregistrer","exit":"Quitter",
  "lang":"Langue","help":"Aide","palette":"Blocs","script":"Script","stage":"Scène",
  "run":"▶ Exécuter","stop":"■ Arrêter","clear":"Effacer",
  "sprites":"Personnages","backdrops":"Arrière-plans",
  "add_sprite":"+ Personnage","add_backdrop":"+ Arrière-plan",
  "edit":"Éditer","upload":"Charger image","delete":"Supprimer",
  "cat_ev":"Événements","cat_mo":"Mouvement","cat_lo":"Apparence","cat_co":"Contrôle",
  "cat_se":"Capteurs","cat_op":"Opérateurs","cat_va":"Variables","cat_pe":"Stylo",
  "saved":"Enregistré:","loaded":"Chargé:","err":"Erreur",
  "newq":"Abandonner le script actuel ?","help_txt":
   "Comment utiliser :\n\n"
   "1. Cliquez sur les blocs à gauche.\n"
   "2. Tab pour indenter dans les blocs C.\n"
   "3. Appuyez sur ▶ Exécuter.\n\n"
   "Personnages et arrière-plans :\n"
   "• '+ Personnage' ajoute un sprite.\n"
   "• 'Éditer' ouvre l'éditeur de pixels.\n"
   "• 'Charger image' charge un GIF/PNG.\n"
   "• Idem pour les arrière-plans.\n\n"
   "Sauvegardez en .sc",
  "ed_title_sprite":"Éditer personnage","ed_title_backdrop":"Éditer arrière-plan",
  "ed_color":"Couleur","ed_eraser":"Gomme","ed_fill":"Remplir","ed_clear":"Effacer",
  "ed_undo":"Annuler","ed_save":"✓ Enregistrer","ed_cancel":"✗ Annuler",
  "ed_palette":"Palette rapide","ed_tools":"Outils",
  "choose_img":"Choisir image","pick_color":"Choisir couleur",
 },
 "ru": {
  "file":"Файл","new":"Новый","open":"Открыть","save":"Сохранить","exit":"Выход",
  "lang":"Язык","help":"Справка","palette":"Блоки","script":"Скрипт","stage":"Сцена",
  "run":"▶ Запуск","stop":"■ Стоп","clear":"Очистить",
  "sprites":"Спрайты","backdrops":"Фоны",
  "add_sprite":"+ Спрайт","add_backdrop":"+ Фон",
  "edit":"Изменить","upload":"Загрузить","delete":"Удалить",
  "cat_ev":"События","cat_mo":"Движение","cat_lo":"Внешность","cat_co":"Управление",
  "cat_se":"Сенсоры","cat_op":"Операторы","cat_va":"Переменные","cat_pe":"Перо",
  "saved":"Сохранено:","loaded":"Загружено:","err":"Ошибка",
  "newq":"Отменить текущий скрипт?","help_txt":
   "Как пользоваться:\n\n"
   "1. Нажимайте блоки слева.\n"
   "2. Tab — отступ внутри C-блоков.\n"
   "3. Нажмите ▶ Запуск.\n\n"
   "Спрайты и фоны:\n"
   "• '+ Спрайт' добавляет спрайт.\n"
   "• 'Изменить' открывает редактор.\n"
   "• 'Загрузить' загружает GIF/PNG.\n"
   "• То же для фонов.\n\n"
   "Сохраняйте в .sc",
  "ed_title_sprite":"Изменить спрайт","ed_title_backdrop":"Изменить фон",
  "ed_color":"Цвет","ed_eraser":"Ластик","ed_fill":"Залить","ed_clear":"Очистить",
  "ed_undo":"Отменить","ed_save":"✓ Сохранить","ed_cancel":"✗ Отмена",
  "ed_palette":"Быстрая палитра","ed_tools":"Инструменты",
  "choose_img":"Выбрать изображение","pick_color":"Выбрать цвет",
 },
 "ja": {
  "file":"ファイル","new":"新規","open":"開く","save":"保存","exit":"終了",
  "lang":"言語","help":"ヘルプ","palette":"ブロック","script":"スクリプト","stage":"ステージ",
  "run":"▶ 実行","stop":"■ 停止","clear":"クリア",
  "sprites":"スプライト","backdrops":"背景",
  "add_sprite":"+ スプライト","add_backdrop":"+ 背景",
  "edit":"編集","upload":"画像を読込","delete":"削除",
  "cat_ev":"イベント","cat_mo":"動き","cat_lo":"見た目","cat_co":"制御",
  "cat_se":"調べる","cat_op":"演算","cat_va":"変数","cat_pe":"ペン",
  "saved":"保存:","loaded":"読込:","err":"エラー",
  "newq":"現在のスクリプトを破棄しますか？","help_txt":
   "使い方:\n\n"
   "1. 左のブロックをクリック。\n"
   "2. Tab で C ブロック内をインデント。\n"
   "3. ▶ 実行で実行。\n\n"
   "スプライトと背景:\n"
   "• '+ スプライト' で追加。\n"
   "• '編集' でピクセルエディタ。\n"
   "• '画像を読込' で GIF/PNG 読込。\n"
   "• 背景も同様。\n\n"
   ".sc で保存。",
  "ed_title_sprite":"スプライト編集","ed_title_backdrop":"背景編集",
  "ed_color":"色","ed_eraser":"消しゴム","ed_fill":"塗りつぶし","ed_clear":"クリア",
  "ed_undo":"元に戻す","ed_save":"✓ 保存","ed_cancel":"✗ キャンセル",
  "ed_palette":"クイックパレット","ed_tools":"ツール",
  "choose_img":"画像を選択","pick_color":"色を選択",
 },
}

# ══════════════════════════════════════════════════════════════════
# 2. BLOQUES (subconjunto representativo de Scratch 3.0)
# ══════════════════════════════════════════════════════════════════
BLOCKS = [
 # EVENTOS
 {"id":"when_flag","cat":"cat_ev","color":"#f9c74f","c":False,
  "kw":{"es":"cuando_bandera","en":"when_flag","pt":"quando_bandeira","fr":"quand_drapeau","ru":"когда_флаг","ja":"ハタ"},
  "tpl":{"es":"cuando_bandera","en":"when_flag","pt":"quando_bandeira","fr":"quand_drapeau","ru":"когда_флаг","ja":"ハタ"}},
 {"id":"broadcast","cat":"cat_ev","color":"#f9c74f","c":False,
  "kw":{"es":"enviar","en":"broadcast","pt":"enviar","fr":"envoyer","ru":"передать","ja":"オクル"},
  "tpl":{"es":"enviar mensaje1","en":"broadcast message1","pt":"enviar mensagem1","fr":"envoyer message1","ru":"передать сообщение1","ja":"オクル メッセージ1"}},
 {"id":"when_receive","cat":"cat_ev","color":"#f9c74f","c":False,
  "kw":{"es":"cuando_recibo","en":"when_receive","pt":"quando_recebo","fr":"quand_recois","ru":"когда_получаю","ja":"ウケトル"},
  "tpl":{"es":"cuando_recibo mensaje1","en":"when_receive message1","pt":"quando_recebo mensagem1","fr":"quand_recois message1","ru":"когда_получаю сообщение1","ja":"ウケトル メッセージ1"}},
 # MOVIMIENTO
 {"id":"move","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"mover","en":"move","pt":"mover","fr":"avancer","ru":"идти","ja":"ウゴク"},
  "tpl":{"es":"mover 10","en":"move 10","pt":"mover 10","fr":"avancer 10","ru":"идти 10","ja":"ウゴク 10"}},
 {"id":"turn_r","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"girar_d","en":"turn_r","pt":"girar_d","fr":"tourner_d","ru":"вправо","ja":"ミギ"},
  "tpl":{"es":"girar_d 15","en":"turn_r 15","pt":"girar_d 15","fr":"tourner_d 15","ru":"вправо 15","ja":"ミギ 15"}},
 {"id":"turn_l","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"girar_i","en":"turn_l","pt":"girar_e","fr":"tourner_g","ru":"влево","ja":"ヒダリ"},
  "tpl":{"es":"girar_i 15","en":"turn_l 15","pt":"girar_e 15","fr":"tourner_g 15","ru":"влево 15","ja":"ヒダリ 15"}},
 {"id":"goto","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"ir_a","en":"goto","pt":"ir_para","fr":"aller_a","ru":"перейти","ja":"イク"},
  "tpl":{"es":"ir_a 0 0","en":"goto 0 0","pt":"ir_para 0 0","fr":"aller_a 0 0","ru":"перейти 0 0","ja":"イク 0 0"}},
 {"id":"glide","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"deslizar","en":"glide","pt":"deslizar","fr":"glisser","ru":"скользить","ja":"スベテ"},
  "tpl":{"es":"deslizar 1 0 0","en":"glide 1 0 0","pt":"deslizar 1 0 0","fr":"glisser 1 0 0","ru":"скользить 1 0 0","ja":"スベテ 1 0 0"}},
 {"id":"point_dir","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"apuntar","en":"point_dir","pt":"apontar","fr":"pointer","ru":"направить","ja":"ムケル"},
  "tpl":{"es":"apuntar 90","en":"point_dir 90","pt":"apontar 90","fr":"pointer 90","ru":"направить 90","ja":"ムケル 90"}},
 {"id":"bounce","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"rebotar","en":"bounce","pt":"rebater","fr":"rebondir","ru":"отскочить","ja":"ハネカエル"},
  "tpl":{"es":"rebotar","en":"bounce","pt":"rebater","fr":"rebondir","ru":"отскочить","ja":"ハネカエル"}},
 {"id":"set_x","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"fijar_x","en":"set_x","pt":"definir_x","fr":"fixer_x","ru":"установить_x","ja":"Xヲ"},
  "tpl":{"es":"fijar_x 0","en":"set_x 0","pt":"definir_x 0","fr":"fixer_x 0","ru":"установить_x 0","ja":"Xヲ 0"}},
 {"id":"set_y","cat":"cat_mo","color":"#4a90d9","c":False,
  "kw":{"es":"fijar_y","en":"set_y","pt":"definir_y","fr":"fixer_y","ru":"установить_y","ja":"Yヲ"},
  "tpl":{"es":"fijar_y 0","en":"set_y 0","pt":"definir_y 0","fr":"fixer_y 0","ru":"установить_y 0","ja":"Yヲ 0"}},
 # APARIENCIA
 {"id":"say","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"decir","en":"say","pt":"dizer","fr":"dire","ru":"сказать","ja":"イウ"},
  "tpl":{"es":'decir "¡Hola!"',"en":'say "Hello!"',"pt":'dizer "Olá!"',"fr":'dire "Bonjour!"',"ru":'сказать "Привет!"',"ja":'イウ "こんにちは"'}},
 {"id":"say_secs","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"decir_por","en":"say_secs","pt":"dizer_por","fr":"dire_pdt","ru":"сказать_сек","ja":"イウビョウ"},
  "tpl":{"es":'decir_por "¡Hola!" 2',"en":'say_secs "Hello!" 2',"pt":'dizer_por "Olá!" 2',"fr":'dire_pdt "Bonjour!" 2',"ru":'сказать_сек "Привет!" 2',"ja":'イウビョウ "こんにちは" 2'}},
 {"id":"think","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"pensar","en":"think","pt":"pensar","fr":"penser","ru":"думать","ja":"オモウ"},
  "tpl":{"es":'pensar "Hmm..."',"en":'think "Hmm..."',"pt":'pensar "Hmm..."',"fr":'penser "Hmm..."',"ru":'думать "Хм..."',"ja":'オモウ "ふむ..."'}},
 {"id":"show","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"mostrar","en":"show","pt":"mostrar","fr":"montrer","ru":"показать","ja":"ミセル"},
  "tpl":{"es":"mostrar","en":"show","pt":"mostrar","fr":"montrer","ru":"показать","ja":"ミセル"}},
 {"id":"hide","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"esconder","en":"hide","pt":"esconder","fr":"cacher","ru":"спрятать","ja":"カクス"},
  "tpl":{"es":"esconder","en":"hide","pt":"esconder","fr":"cacher","ru":"спрятать","ja":"カクス"}},
 {"id":"change_size","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"cambiar_tamano","en":"change_size","pt":"mudar_tamanho","fr":"changer_taille","ru":"изменить_размер","ja":"オオキサカエル"},
  "tpl":{"es":"cambiar_tamano 10","en":"change_size 10","pt":"mudar_tamanho 10","fr":"changer_taille 10","ru":"изменить_размер 10","ja":"オオキサカエル 10"}},
 {"id":"set_size","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"fijar_tamano","en":"set_size","pt":"definir_tamanho","fr":"fixer_taille","ru":"установить_размер","ja":"オオキサ"},
  "tpl":{"es":"fijar_tamano 100","en":"set_size 100","pt":"definir_tamanho 100","fr":"fixer_taille 100","ru":"установить_размер 100","ja":"オオキサ 100"}},
 {"id":"switch_backdrop","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"cambiar_fondo","en":"switch_backdrop","pt":"mudar_cenario","fr":"changer_arriereplan","ru":"сменить_фон","ja":"ハイケイ"},
  "tpl":{"es":"cambiar_fondo fondo1","en":"switch_backdrop backdrop1","pt":"mudar_cenario cenario1","fr":"changer_arriereplan arriere1","ru":"сменить_фон фон1","ja":"ハイケイ ハイケイ1"}},
 {"id":"next_backdrop","cat":"cat_lo","color":"#9d4edd","c":False,
  "kw":{"es":"siguiente_fondo","en":"next_backdrop","pt":"proximo_cenario","fr":"arriereplan_suivant","ru":"следующий_фон","ja":"ツギノハイケイ"},
  "tpl":{"es":"siguiente_fondo","en":"next_backdrop","pt":"proximo_cenario","fr":"arriereplan_suivant","ru":"следующий_фон","ja":"ツギノハイケイ"}},
 # CONTROL
 {"id":"wait","cat":"cat_co","color":"#f77f00","c":False,
  "kw":{"es":"esperar","en":"wait","pt":"esperar","fr":"attendre","ru":"ждать","ja":"マツ"},
  "tpl":{"es":"esperar 1","en":"wait 1","pt":"esperar 1","fr":"attendre 1","ru":"ждать 1","ja":"マツ 1"}},
 {"id":"repeat","cat":"cat_co","color":"#f77f00","c":True,
  "kw":{"es":"repetir","en":"repeat","pt":"repetir","fr":"repeter","ru":"повторить","ja":"クリカエス"},
  "tpl":{"es":"repetir 4","en":"repeat 4","pt":"repetir 4","fr":"repeter 4","ru":"повторить 4","ja":"クリカエス 4"}},
 {"id":"forever","cat":"cat_co","color":"#f77f00","c":True,
  "kw":{"es":"por_siempre","en":"forever","pt":"sempre","fr":"toujours","ru":"всегда","ja":"ズット"},
  "tpl":{"es":"por_siempre","en":"forever","pt":"sempre","fr":"toujours","ru":"всегда","ja":"ズット"}},
 {"id":"if_then","cat":"cat_co","color":"#f77f00","c":True,
  "kw":{"es":"si","en":"if_then","pt":"se","fr":"si","ru":"если","ja":"モシ"},
  "tpl":{"es":"si 1=1","en":"if_then 1=1","pt":"se 1=1","fr":"si 1=1","ru":"если 1=1","ja":"モシ 1=1"}},
 {"id":"wait_until","cat":"cat_co","color":"#f77f00","c":False,
  "kw":{"es":"esperar_hasta","en":"wait_until","pt":"esperar_ate","fr":"attendre_jusqua","ru":"ждать_до","ja":"マツマデ"},
  "tpl":{"es":"esperar_hasta 1=1","en":"wait_until 1=1","pt":"esperar_ate 1=1","fr":"attendre_jusqua 1=1","ru":"ждать_до 1=1","ja":"マツマデ 1=1"}},
 {"id":"stop","cat":"cat_co","color":"#f77f00","c":False,
  "kw":{"es":"parar","en":"stop","pt":"parar","fr":"arreter","ru":"стоп","ja":"ストップ"},
  "tpl":{"es":"parar todos","en":"stop all","pt":"parar todos","fr":"arreter tous","ru":"стоп все","ja":"ストップ スベテ"}},
 # SENSORES
 {"id":"touching","cat":"cat_se","color":"#5bc0eb","c":False,"reporter":True,
  "kw":{"es":"tocando","en":"touching","pt":"tocando","fr":"touche","ru":"касается","ja":"フレル"},
  "tpl":{"es":"tocando borde","en":"touching edge","pt":"tocando borda","fr":"touche bord","ru":"касается край","ja":"フレル ハシ"}},
 {"id":"ask","cat":"cat_se","color":"#5bc0eb","c":False,
  "kw":{"es":"preguntar","en":"ask","pt":"perguntar","fr":"demander","ru":"спросить","ja":"キク"},
  "tpl":{"es":'preguntar "¿Nombre?"',"en":'ask "Name?"',"pt":'perguntar "Nome?"',"fr":'demander "Nom ?"',"ru":'спросить "Имя?"',"ja":'キク "ナマエ?"'}},
 {"id":"timer","cat":"cat_se","color":"#5bc0eb","c":False,"reporter":True,
  "kw":{"es":"cronometro","en":"timer","pt":"cronometro","fr":"chronometre","ru":"таймер","ja":"タイマー"},
  "tpl":{"es":"cronometro","en":"timer","pt":"cronometro","fr":"chronometre","ru":"таймер","ja":"タイマー"}},
 # OPERADORES
 {"id":"add","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"sumar","en":"add","pt":"somar","fr":"ajouter","ru":"сложить","ja":"タス"},
  "tpl":{"es":"sumar 1 2","en":"add 1 2","pt":"somar 1 2","fr":"ajouter 1 2","ru":"сложить 1 2","ja":"タス 1 2"}},
 {"id":"sub","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"restar","en":"sub","pt":"subtrair","fr":"soustraire","ru":"вычесть","ja":"ヒク"},
  "tpl":{"es":"restar 1 2","en":"sub 1 2","pt":"subtrair 1 2","fr":"soustraire 1 2","ru":"вычесть 1 2","ja":"ヒク 1 2"}},
 {"id":"mul","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"multiplicar","en":"mul","pt":"multiplicar","fr":"multiplier","ru":"умножить","ja":"カケル"},
  "tpl":{"es":"multiplicar 1 2","en":"mul 1 2","pt":"multiplicar 1 2","fr":"multiplier 1 2","ru":"умножить 1 2","ja":"カケル 1 2"}},
 {"id":"div","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"dividir","en":"div","pt":"dividir","fr":"diviser","ru":"разделить","ja":"ワル"},
  "tpl":{"es":"dividir 1 2","en":"div 1 2","pt":"dividir 1 2","fr":"diviser 1 2","ru":"разделить 1 2","ja":"ワル 1 2"}},
 {"id":"random","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"aleatorio","en":"random","pt":"aleatorio","fr":"aleatoire","ru":"случайное","ja":"ランダム"},
  "tpl":{"es":"aleatorio 1 10","en":"random 1 10","pt":"aleatorio 1 10","fr":"aleatoire 1 10","ru":"случайное 1 10","ja":"ランダム 1 10"}},
 {"id":"join","cat":"cat_op","color":"#43aa8b","c":False,"reporter":True,
  "kw":{"es":"unir","en":"join","pt":"juntar","fr":"joindre","ru":"объединить","ja":"ツナグ"},
  "tpl":{"es":'unir "a" "b"',"en":'join "a" "b"',"pt":'juntar "a" "b"',"fr":'joindre "a" "b"',"ru":'объединить "a" "b"',"ja":'ツナグ "a" "b"'}},
 # VARIABLES
 {"id":"set_var","cat":"cat_va","color":"#e07a5f","c":False,
  "kw":{"es":"fijar","en":"set_var","pt":"definir","fr":"fixer","ru":"установить","ja":"セット"},
  "tpl":{"es":"fijar mi_var 0","en":"set_var my_var 0","pt":"definir minha_var 0","fr":"fixer ma_var 0","ru":"установить моя_перем 0","ja":"セット ワタシノヘンスウ 0"}},
 {"id":"change_var","cat":"cat_va","color":"#e07a5f","c":False,
  "kw":{"es":"cambiar","en":"change_var","pt":"mudar","fr":"changer","ru":"изменить","ja":"カエル"},
  "tpl":{"es":"cambiar mi_var 1","en":"change_var my_var 1","pt":"mudar minha_var 1","fr":"changer ma_var 1","ru":"изменить моя_перем 1","ja":"カエル ワタシノヘンスウ 1"}},
 # LÁPIZ
 {"id":"pen_down","cat":"cat_pe","color":"#2d6a4f","c":False,
  "kw":{"es":"bajar_lapiz","en":"pen_down","pt":"abaixar_caneta","fr":"stylo_baisse","ru":"опустить_перо","ja":"ペンオロス"},
  "tpl":{"es":"bajar_lapiz","en":"pen_down","pt":"abaixar_caneta","fr":"stylo_baisse","ru":"опустить_перо","ja":"ペンオロス"}},
 {"id":"pen_up","cat":"cat_pe","color":"#2d6a4f","c":False,
  "kw":{"es":"subir_lapiz","en":"pen_up","pt":"levantar_caneta","fr":"stylo_leve","ru":"поднять_перо","ja":"ペンアゲル"},
  "tpl":{"es":"subir_lapiz","en":"pen_up","pt":"levantar_caneta","fr":"stylo_leve","ru":"поднять_перо","ja":"ペンアゲル"}},
 {"id":"pen_clear","cat":"cat_pe","color":"#2d6a4f","c":False,
  "kw":{"es":"borrar_lapiz","en":"pen_clear","pt":"limpar_caneta","fr":"effacer_stylo","ru":"очистить_перо","ja":"ペンクリア"},
  "tpl":{"es":"borrar_lapiz","en":"pen_clear","pt":"limpar_caneta","fr":"effacer_stylo","ru":"очистить_перо","ja":"ペンクリア"}},
 {"id":"set_pen_color","cat":"cat_pe","color":"#2d6a4f","c":False,
  "kw":{"es":"color_lapiz","en":"set_pen_color","pt":"cor_caneta","fr":"couleur_stylo","ru":"цвет_пера","ja":"ペンイロ"},
  "tpl":{"es":"color_lapiz #ff0000","en":"set_pen_color #ff0000","pt":"cor_caneta #ff0000","fr":"couleur_stylo #ff0000","ru":"цвет_пера #ff0000","ja":"ペンイロ #ff0000"}},
 {"id":"set_pen_size","cat":"cat_pe","color":"#2d6a4f","c":False,
  "kw":{"es":"tamano_lapiz","en":"set_pen_size","pt":"tamanho_caneta","fr":"taille_stylo","ru":"размер_пера","ja":"ペンサイズ"},
  "tpl":{"es":"tamano_lapiz 2","en":"set_pen_size 2","pt":"tamanho_caneta 2","fr":"taille_stylo 2","ru":"размер_пера 2","ja":"ペンサイズ 2"}},
]
KW_TO_ID = {k: b["id"] for b in BLOCKS for k in b["kw"].values()}

# ══════════════════════════════════════════════════════════════════
# 3. PARSER
# ══════════════════════════════════════════════════════════════════
def parse_script(text):
    return _parse_block(text.split("\n"), 0, -1)[0]

def _parse_block(lines, i, parent_indent):
    out = []
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            i += 1; continue
        indent = len(raw) - len(raw.lstrip(" \t"))
        if indent <= parent_indent: break
        parts = raw.strip().split(None, 1)
        kw = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        bid = KW_TO_ID.get(kw)
        if bid is None:
            i += 1; continue
        block_def = next(b for b in BLOCKS if b["id"] == bid)
        if block_def.get("c"):
            body, i2 = _parse_block(lines, i+1, indent)
            out.append((bid, [rest], body)); i = i2
        else:
            out.append((bid, [rest], [])); i += 1
    return out, i

# ══════════════════════════════════════════════════════════════════
# 4. SPRITE  (con soporte para imagen dibujada o subida)
# ══════════════════════════════════════════════════════════════════
class Sprite:
    def __init__(self, canvas, name="Sprite1", x=0, y=0, color="#4a90d9"):
        self.c = canvas
        self.name = name
        self.x = float(x); self.y = float(y)
        self.direction = 90.0
        self.color = color
        self.scale = 100.0
        self.visible = True
        self.image = None           # tk.PhotoImage (dibujada o subida)
        self.image_data = None      # para guardar en .sc (lista de píxeles)
        self.canvas_items = []
        self.bubble = None
        self.draw()

    def _coords(self):
        return 250 + self.x, 200 - self.y

    def _size(self):
        return max(4, int(16 * self.scale / 100.0))

    def draw(self):
        for it in self.canvas_items:
            self.c.delete(it)
        self.canvas_items = []
        if not self.visible:
            return
        cx, cy = self._coords()
        if self.image:
            self.canvas_items.append(
                self.c.create_image(cx, cy, image=self.image, anchor="center"))
        else:
            r = self._size()
            rad = math.radians(self.direction)
            pts = []
            for a in (0, 2.5, -2.5):
                pts += [cx + r*math.cos(rad + a), cy - r*math.sin(rad + a)]
            self.canvas_items.append(
                self.c.create_polygon(pts, fill=self.color, outline="#222", width=2))

    def move(self, steps):
        rad = math.radians(self.direction)
        self.x += float(steps) * math.cos(rad)
        self.y += float(steps) * math.sin(rad)
        self.draw()

    def turn(self, deg):
        self.direction = (self.direction + float(deg)) % 360
        self.draw()

    def goto(self, x, y):
        self.x, self.y = float(x), float(y); self.draw()

    def glide(self, secs, x, y):
        secs = max(0.05, float(secs))
        x0, y0 = self.x, self.y
        steps = max(1, int(secs / 0.02))
        for k in range(1, steps+1):
            t = k / steps
            self.x = x0 + (float(x)-x0)*t
            self.y = y0 + (float(y)-y0)*t
            self.draw()
            time.sleep(secs/steps)

    def say(self, msg):
        self.clear_bubble()
        cx, cy = self._coords()
        self.bubble = self.c.create_text(cx, cy - self._size() - 20,
                                         text=str(msg), font=("Segoe UI", 11, "bold"),
                                         fill="#111")

    def clear_bubble(self):
        if self.bubble:
            self.c.delete(self.bubble); self.bubble = None

    def set_color(self, c):
        self.color = c; self.draw()

    def set_scale(self, s):
        self.scale = max(1, min(500, float(s))); self.draw()

    def set_image(self, img):
        self.image = img; self.draw()

    def show(self):
        self.visible = True; self.draw()

    def hide(self):
        self.visible = False; self.draw()

    def reset(self):
        self.x = self.y = 0.0; self.direction = 90.0
        self.scale = 100.0; self.visible = True
        self.clear_bubble(); self.draw()

# ══════════════════════════════════════════════════════════════════
# 5. EDITOR DE PÍXELES (dibujo píxel a píxel con el ratón)
# ══════════════════════════════════════════════════════════════════
class PixelEditor(tk.Toplevel):
    """
    Editor visual de imágenes: el usuario dibuja píxel a píxel con el ratón.
    Devuelve una tk.PhotoImage en self.result.
    """
    def __init__(self, parent, w, h, cell, lang, title):
        super().__init__(parent)
        self.title(title)
        self.w = w; self.h = h; self.cell = cell
        self.lang = lang
        self.grid = [["" for _ in range(w)] for _ in range(h)]
        self.current_color = "#000000"
        self.history = []
        self.result = None
        self._build()
        self._redraw_all()
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _build(self):
        tr = T[self.lang]
        # Canvas izquierda
        left = tk.Frame(self); left.pack(side=tk.LEFT, padx=8, pady=8)
        self.canvas = tk.Canvas(left, width=self.w*self.cell, height=self.h*self.cell,
                                 bg="white", highlightthickness=1, highlightbackground="#888")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._paint)
        self.canvas.bind("<B1-Motion>", self._paint)

        # Panel derecho
        right = tk.Frame(self); right.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        tk.Label(right, text=tr["ed_tools"], font=("Segoe UI", 10, "bold")).pack(pady=(0,4))

        tk.Button(right, text=tr["ed_color"], command=self._pick_color,
                  width=14).pack(pady=2)
        self.color_preview = tk.Label(right, bg=self.current_color, width=14, height=2,
                                       relief="solid", borderwidth=1)
        self.color_preview.pack(pady=2)

        self.eraser_var = tk.BooleanVar()
        tk.Checkbutton(right, text=tr["ed_eraser"], variable=self.eraser_var,
                        width=14).pack(pady=2)

        tk.Button(right, text=tr["ed_fill"], command=self._fill, width=14).pack(pady=2)
        tk.Button(right, text=tr["ed_clear"], command=self._clear, width=14).pack(pady=2)
        tk.Button(right, text=tr["ed_undo"], command=self._undo, width=14).pack(pady=2)

        tk.Label(right, text=tr["ed_palette"], font=("Segoe UI", 10, "bold")).pack(pady=(8,4))
        palette = ["#000000","#ffffff","#ff0000","#00ff00","#0000ff",
                   "#ffff00","#ff00ff","#00ffff","#ff8800","#8800ff",
                   "#888888","#444444","#8b4513","#ffc0cb","#008080","#ffa500"]
        pf = tk.Frame(right); pf.pack()
        for i, c in enumerate(palette):
            tk.Button(pf, bg=c, width=3, height=1,
                      command=lambda col=c: self._set_color(col)
                      ).grid(row=i//4, column=i%4, padx=1, pady=1)

        tk.Frame(right, height=10).pack()

        tk.Button(right, text=tr["ed_save"], command=self._save, width=14,
                  bg="#4CAF50", fg="white",
                  font=("Segoe UI", 10, "bold")).pack(pady=2)
        tk.Button(right, text=tr["ed_cancel"], command=self._cancel,
                  width=14).pack(pady=2)

    # ── pintar ──
    def _paint(self, event):
        x = event.x // self.cell
        y = event.y // self.cell
        if 0 <= x < self.w and 0 <= y < self.h:
            self.history.append((x, y, self.grid[y][x]))
            self.grid[y][x] = "" if self.eraser_var.get() else self.current_color
            self._draw_cell(x, y)

    def _draw_cell(self, x, y):
        x0, y0 = x*self.cell, y*self.cell
        x1, y1 = x0+self.cell, y0+self.cell
        c = self.grid[y][x] or "white"
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=c, outline="#ddd")

    def _redraw_all(self):
        self.canvas.delete("all")
        for y in range(self.h):
            for x in range(self.w):
                self._draw_cell(x, y)

    # ── herramientas ──
    def _pick_color(self):
        c = colorchooser.askcolor(color=self.current_color, title=T[self.lang]["pick_color"])[1]
        if c:
            self.current_color = c
            self.color_preview.config(bg=c)
            self.eraser_var.set(False)

    def _set_color(self, c):
        self.current_color = c
        self.color_preview.config(bg=c)
        self.eraser_var.set(False)

    def _fill(self):
        for y in range(self.h):
            for x in range(self.w):
                self.history.append((x, y, self.grid[y][x]))
                self.grid[y][x] = self.current_color
        self._redraw_all()

    def _clear(self):
        for y in range(self.h):
            for x in range(self.w):
                self.history.append((x, y, self.grid[y][x]))
                self.grid[y][x] = ""
        self._redraw_all()

    def _undo(self):
        if self.history:
            x, y, c = self.history.pop()
            self.grid[y][x] = c
            self._draw_cell(x, y)

    # ── generar imagen ──
    def to_photoimage(self):
        img = tk.PhotoImage(width=self.w, height=self.h)
        for y in range(self.h):
            for x in range(self.w):
                c = self.grid[y][x]
                if c:
                    img.put(c, to=(x, y, x+1, y+1))
        return img

    def _save(self):
        self.result = self.to_photoimage()
        self.result_grid = [row[:] for row in self.grid]
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()

# ══════════════════════════════════════════════════════════════════
# 6. UTILIDADES DE IMAGEN
# ══════════════════════════════════════════════════════════════════
def load_photoimage(path, max_w, max_h):
    """Carga una imagen y la ajusta al tamaño máximo indicado."""
    img = tk.PhotoImage(file=path)
    w, h = img.width(), img.height()
    if w > max_w or h > max_h:
        f = max(w // max_w + 1, h // max_h + 1)
        img = img.subsample(f, f)
    return img

def image_to_grid(img, w, h):
    """Convierte una PhotoImage en una rejilla de colores (para re-editar)."""
    grid = [["" for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            try:
                c = img.get(x, y)
                if isinstance(c, tuple):
                    c = "#{:02x}{:02x}{:02x}".format(int(c[0]), int(c[1]), int(c[2]))
                if c and c not in ("#ffffff", "white"):
                    grid[y][x] = c
            except Exception:
                pass
    return grid

def grid_to_photoimage(grid, w, h):
    """Convierte una rejilla de colores en PhotoImage."""
    img = tk.PhotoImage(width=w, height=h)
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if c:
                img.put(c, to=(x, y, x+1, y+1))
    return img

# ══════════════════════════════════════════════════════════════════
# 7. APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════
SPRITE_GRID = (40, 40)     # ancho x alto en píxeles del editor de sprite
SPRITE_CELL = 12           # píxeles por celda en pantalla
BACKDROP_GRID = (50, 40)   # ancho x alto en píxeles del editor de fondo
BACKDROP_CELL = 10         # píxeles por celda en pantalla
STAGE_W, STAGE_H = 500, 400

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1300x820")
        self.lang = "es"
        self.running = False
        self.stop_flag = False
        self.sprites = []
        self.current_sprite = None
        self.backdrops = []          # lista de dicts {name, image, grid}
        self.backdrop_item = None
        self.pen_active = False
        self.pen_color = "#ff0000"
        self.pen_size = 2
        self.pen_lines = []
        self.pen_last = None
        self.variables = {}
        self._build()
        self._apply_lang()
        self._add_default_backdrop()
        self.add_sprite()

    # ── Construcción ──
    def _build(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Barra superior
        top = tk.Frame(self.root); top.pack(fill=tk.X, padx=8, pady=6)
        self.btn_run = tk.Button(top, command=self.run_script, bg="#4CAF50",
                                 fg="white", font=("Segoe UI", 10, "bold"), padx=10)
        self.btn_run.pack(side=tk.LEFT, padx=2)
        self.btn_stop = tk.Button(top, command=self.stop_script, bg="#e63946",
                                  fg="white", font=("Segoe UI", 10, "bold"),
                                  padx=10, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=2)
        self.btn_clear = tk.Button(top, command=self.clear_script, padx=10)
        self.btn_clear.pack(side=tk.LEFT, padx=2)

        # Layout principal
        main = tk.Frame(self.root); main.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Paleta
        self.left = tk.LabelFrame(main)
        self.left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,4))
        self.palette_canvas = tk.Canvas(self.left, width=210, highlightthickness=0)
        self.palette_scroll = tk.Scrollbar(self.left, orient="vertical",
                                            command=self.palette_canvas.yview)
        self.palette_inner = tk.Frame(self.palette_canvas)
        self.palette_inner.bind("<Configure>",
            lambda e: self.palette_canvas.configure(scrollregion=self.palette_canvas.bbox("all")))
        self.palette_canvas.create_window((0,0), window=self.palette_inner, anchor="nw")
        self.palette_canvas.configure(yscrollcommand=self.palette_scroll.set)
        self.palette_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.palette_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Guion
        self.center = tk.LabelFrame(main)
        self.center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        self.script_text = tk.Text(self.center, font=("Consolas", 11), undo=True,
                                    bg="#fafafa", insertbackground="#222", wrap=tk.NONE)
        self.script_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.script_text.bind("<Tab>", lambda e: (self.script_text.insert(tk.INSERT, "    "), "break")[1])

        # Derecha: escenario + propiedades
        right = tk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, padx=(4,0))

        self.right = tk.LabelFrame(right)
        self.right.pack(fill=tk.X)
        self.stage = tk.Canvas(self.right, width=STAGE_W, height=STAGE_H, bg="white",
                                highlightthickness=1, highlightbackground="#ccc")
        self.stage.pack(padx=6, pady=6)
        self.stage.create_line(0, 200, STAGE_W, 200, fill="#eee")
        self.stage.create_line(250, 0, 250, STAGE_H, fill="#eee")

        # Panel de personajes
        self.sprites_frame = tk.LabelFrame(right)
        self.sprites_frame.pack(fill=tk.X, pady=(6,0))
        sf = tk.Frame(self.sprites_frame); sf.pack(fill=tk.X, padx=4, pady=4)
        self.sprite_listbox = tk.Listbox(sf, height=4, exportselection=False)
        self.sprite_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.sprite_listbox.bind("<<ListboxSelect>>", self._on_sprite_select)
        sbtns = tk.Frame(sf); sbtns.pack(side=tk.LEFT, padx=4)
        self.btn_add_sprite = tk.Button(sbtns, command=self.add_sprite, width=12)
        self.btn_add_sprite.pack(pady=1)
        self.btn_edit_sprite = tk.Button(sbtns, command=self.edit_sprite, width=12)
        self.btn_edit_sprite.pack(pady=1)
        self.btn_upload_sprite = tk.Button(sbtns, command=self.upload_sprite_image, width=12)
        self.btn_upload_sprite.pack(pady=1)
        self.btn_del_sprite = tk.Button(sbtns, command=self.delete_sprite, width=12)
        self.btn_del_sprite.pack(pady=1)

        # Panel de fondos
        self.bd_frame = tk.LabelFrame(right)
        self.bd_frame.pack(fill=tk.X, pady=(6,0))
        bf = tk.Frame(self.bd_frame); bf.pack(fill=tk.X, padx=4, pady=4)
        self.bd_listbox = tk.Listbox(bf, height=3, exportselection=False)
        self.bd_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.bd_listbox.bind("<<ListboxSelect>>", self._on_backdrop_select)
        bbtns = tk.Frame(bf); bbtns.pack(side=tk.LEFT, padx=4)
        self.btn_add_bd = tk.Button(bbtns, command=self.add_backdrop, width=12)
        self.btn_add_bd.pack(pady=1)
        self.btn_edit_bd = tk.Button(bbtns, command=self.edit_backdrop, width=12)
        self.btn_edit_bd.pack(pady=1)
        self.btn_upload_bd = tk.Button(bbtns, command=self.upload_backdrop_image, width=12)
        self.btn_upload_bd.pack(pady=1)

        # Estado
        self.status = tk.Label(self.root, anchor="w", font=("Segoe UI", 9),
                                fg="#555", padx=10)
        self.status.pack(fill=tk.X)

        self._build_palette()

    def _build_palette(self):
        for w in self.palette_inner.winfo_children():
            w.destroy()
        self.palette_widgets = []
        cats = {}
        for b in BLOCKS: cats.setdefault(b["cat"], []).append(b)
        for cat_id, blist in cats.items():
            lbl = tk.Label(self.palette_inner, font=("Segoe UI", 10, "bold"),
                            fg="#333", anchor="w")
            lbl.pack(fill=tk.X, padx=2, pady=(8,2))
            lbl._cat_id = cat_id
            self.palette_widgets.append(lbl)
            for b in blist:
                btn = tk.Button(self.palette_inner, anchor="w", font=("Consolas", 8),
                                 bg=b["color"], fg="white", relief="raised",
                                 cursor="hand2", padx=6, pady=2, wraplength=190,
                                 justify="left",
                                 command=lambda bid=b["id"]: self.insert_block(bid))
                btn.pack(fill=tk.X, padx=2, pady=1)
                btn._bid = b["id"]
                self.palette_widgets.append(btn)

    def insert_block(self, bid):
        block = next(b for b in BLOCKS if b["id"] == bid)
        tpl = block["tpl"][self.lang]
        idx = self.script_text.index(tk.INSERT)
        line = idx.split(".")[0]
        lt = self.script_text.get(f"{line}.0", f"{line}.end")
        indent = len(lt) - len(lt.lstrip(" "))
        if lt.strip():
            self.script_text.insert(f"{line}.end", "\n" + " "*indent + tpl)
        else:
            self.script_text.insert(f"{line}.end", " "*indent + tpl)
        self.script_text.see(tk.INSERT)

    def _apply_lang(self):
        tr = T[self.lang]
        self.root.title("Scratch Code")
        self.menubar.delete(0, tk.END)
        mf = tk.Menu(self.menubar, tearoff=0)
        mf.add_command(label=tr["new"], command=self.new_file)
        mf.add_command(label=tr["open"], command=self.open_file)
        mf.add_command(label=tr["save"], command=self.save_file)
        mf.add_separator()
        mf.add_command(label=tr["exit"], command=self.root.destroy)
        self.menubar.add_cascade(label=tr["file"], menu=mf)
        ml = tk.Menu(self.menubar, tearoff=0)
        for lg in LANGS:
            ml.add_command(label=LANG_NAMES[lg],
                            command=lambda l=lg: self.set_lang(l))
        self.menubar.add_cascade(label=tr["lang"], menu=ml)
        mh = tk.Menu(self.menubar, tearoff=0)
        mh.add_command(label=tr["help"],
                        command=lambda: messagebox.showinfo(tr["help"], tr["help_txt"]))
        self.menubar.add_cascade(label=tr["help"], menu=mh)

        self.btn_run.config(text=tr["run"])
        self.btn_stop.config(text=tr["stop"])
        self.btn_clear.config(text=tr["clear"])
        self.left.config(text=tr["palette"])
        self.center.config(text=tr["script"])
        self.right.config(text=tr["stage"])
        self.sprites_frame.config(text=tr["sprites"])
        self.bd_frame.config(text=tr["backdrops"])
        self.btn_add_sprite.config(text=tr["add_sprite"])
        self.btn_edit_sprite.config(text=tr["edit"])
        self.btn_upload_sprite.config(text=tr["upload"])
        self.btn_del_sprite.config(text=tr["delete"])
        self.btn_add_bd.config(text=tr["add_backdrop"])
        self.btn_edit_bd.config(text=tr["edit"])
        self.btn_upload_bd.config(text=tr["upload"])

        for w in self.palette_widgets:
            if hasattr(w, "_cat_id"):
                w.config(text=tr[w._cat_id])
            elif hasattr(w, "_bid"):
                b = next(b for b in BLOCKS if b["id"] == w._bid)
                w.config(text=b["tpl"][self.lang])

    def set_lang(self, lg):
        self.lang = lg
        self._apply_lang()
        self._refresh_sprite_list()
        self._refresh_backdrop_list()

    # ── Sprites ──
    def add_sprite(self):
        n = len(self.sprites) + 1
        colors = ["#4a90d9","#e63946","#43aa8b","#f9c74f","#9d4edd",
                  "#ff66a3","#f77f00","#2d6a4f"]
        s = Sprite(self.stage, name=f"Sprite{n}", x=0, y=0,
                   color=colors[(n-1) % len(colors)])
        self.sprites.append(s)
        self.current_sprite = s
        self._refresh_sprite_list()
        self.sprite_listbox.selection_clear(0, tk.END)
        self.sprite_listbox.selection_set(len(self.sprites)-1)

    def edit_sprite(self):
        if not self.current_sprite: return
        s = self.current_sprite
        w, h = SPRITE_GRID
        ed = PixelEditor(self.root, w, h, SPRITE_CELL, self.lang,
                          T[self.lang]["ed_title_sprite"])
        if s.image:
            # precargar los píxeles existentes si es posible
            try:
                ed.grid = image_to_grid(s.image, w, h)
                ed._redraw_all()
            except Exception:
                pass
        self.root.wait_window(ed)
        if ed.result:
            s.set_image(ed.result)
            s.image_data = getattr(ed, "result_grid", None)

    def upload_sprite_image(self):
        if not self.current_sprite: return
        path = filedialog.askopenfilename(
            title=T[self.lang]["choose_img"],
            filetypes=[("Imágenes", "*.gif *.png *.ppm *.pgm"),
                       ("Todos", "*.*")])
        if not path: return
        try:
            img = load_photoimage(path, STAGE_W, STAGE_H)
            self.current_sprite.set_image(img)
            self.current_sprite.image_data = None
        except Exception as e:
            messagebox.showerror(T[self.lang]["err"], str(e))

    def delete_sprite(self):
        if not self.sprites: return
        idx = self.sprite_listbox.curselection()
        if not idx: return
        s = self.sprites.pop(idx[0])
        for it in s.canvas_items:
            self.stage.delete(it)
        if s.bubble: self.stage.delete(s.bubble)
        self.current_sprite = self.sprites[-1] if self.sprites else None
        self._refresh_sprite_list()

    def _on_sprite_select(self, event):
        idx = self.sprite_listbox.curselection()
        if idx:
            self.current_sprite = self.sprites[idx[0]]

    def _refresh_sprite_list(self):
        self.sprite_listbox.delete(0, tk.END)
        for s in self.sprites:
            tag = " 🎨" if s.image else ""
            self.sprite_listbox.insert(tk.END, s.name + tag)

    # ── Fondos ──
    def _add_default_backdrop(self):
        # Fondo blanco generado por código (sin imagen externa)
        self.backdrops.append({"name":"Blanco", "image":None, "grid":None})
        self._refresh_backdrop_list()
        self.bd_listbox.selection_set(0)
        self._set_backdrop(0)

    def add_backdrop(self):
        w, h = BACKDROP_GRID
        ed = PixelEditor(self.root, w, h, BACKDROP_CELL, self.lang,
                          T[self.lang]["ed_title_backdrop"])
        self.root.wait_window(ed)
        if ed.result:
            # Zoom para cubrir el escenario
            zoom_f = max(1, STAGE_W // w)
            img = ed.result.zoom(zoom_f, zoom_f) if zoom_f > 1 else ed.result
            name = f"Fondo {len(self.backdrops)+1}"
            self.backdrops.append({"name":name, "image":img,
                                    "grid":getattr(ed, "result_grid", None)})
            self._refresh_backdrop_list()
            self.bd_listbox.selection_clear(0, tk.END)
            self.bd_listbox.selection_set(len(self.backdrops)-1)
            self._set_backdrop(len(self.backdrops)-1)

    def edit_backdrop(self):
        idx = self.bd_listbox.curselection()
        if not idx: return
        i = idx[0]
        bd = self.backdrops[i]
        w, h = BACKDROP_GRID
        ed = PixelEditor(self.root, w, h, BACKDROP_CELL, self.lang,
                          T[self.lang]["ed_title_backdrop"])
        if bd.get("grid"):
            ed.grid = [row[:] for row in bd["grid"]]
            ed._redraw_all()
        elif bd.get("image"):
            try:
                # Reducir para poder editar: subsample si es necesario
                src = bd["image"]
                f = max(1, src.width() // w)
                small = src.subsample(f, f) if f > 1 else src
                ed.grid = image_to_grid(small, w, h)
                ed._redraw_all()
            except Exception:
                pass
        self.root.wait_window(ed)
        if ed.result:
            zoom_f = max(1, STAGE_W // w)
            img = ed.result.zoom(zoom_f, zoom_f) if zoom_f > 1 else ed.result
            bd["image"] = img
            bd["grid"] = getattr(ed, "result_grid", None)
            bd["name"] = bd["name"].split(" ✎")[0] + " ✎"
            self._refresh_backdrop_list()
            self.bd_listbox.selection_set(i)
            self._set_backdrop(i)

    def upload_backdrop_image(self):
        path = filedialog.askopenfilename(
            title=T[self.lang]["choose_img"],
            filetypes=[("Imágenes", "*.gif *.png *.ppm *.pgm"),
                       ("Todos", "*.*")])
        if not path: return
        try:
            img = load_photoimage(path, STAGE_W, STAGE_H)
            name = os.path.basename(path)
            self.backdrops.append({"name":name, "image":img, "grid":None})
            self._refresh_backdrop_list()
            self.bd_listbox.selection_clear(0, tk.END)
            self.bd_listbox.selection_set(len(self.backdrops)-1)
            self._set_backdrop(len(self.backdrops)-1)
        except Exception as e:
            messagebox.showerror(T[self.lang]["err"], str(e))

    def _on_backdrop_select(self, event):
        idx = self.bd_listbox.curselection()
        if idx:
            self._set_backdrop(idx[0])

    def _set_backdrop(self, i):
        if self.backdrop_item:
            self.stage.delete(self.backdrop_item)
            self.backdrop_item = None
        bd = self.backdrops[i]
        img = bd.get("image")
        if img:
            self.backdrop_item = self.stage.create_image(0, 0, image=img, anchor="nw")
            self.stage.tag_lower(self.backdrop_item)
        else:
            self.backdrop_item = self.stage.create_rectangle(
                0, 0, STAGE_W, STAGE_H, fill="white", outline="")
            self.stage.tag_lower(self.backdrop_item)

    def _refresh_backdrop_list(self):
        self.bd_listbox.delete(0, tk.END)
        for bd in self.backdrops:
            self.bd_listbox.insert(tk.END, bd["name"])

    # ── Archivo ──
    def new_file(self):
        if self.script_text.get("1.0", tk.END).strip():
            if not messagebox.askyesno(T[self.lang]["new"], T[self.lang]["newq"]):
                return
        self.script_text.delete("1.0", tk.END)
        for s in self.sprites: s.reset()

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Scratch Code", "*.sc"), ("Todos", "*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert("1.0", data.get("script", ""))
            if data.get("language") in LANGS:
                self.set_lang(data["language"])
            # Reconstruir fondos (solo los que tengan grid)
            for bd_data in data.get("backdrops", []):
                if bd_data.get("grid"):
                    w, h = BACKDROP_GRID
                    img = grid_to_photoimage(bd_data["grid"], w, h)
                    zoom_f = max(1, STAGE_W // w)
                    img = img.zoom(zoom_f, zoom_f) if zoom_f > 1 else img
                    self.backdrops.append({"name": bd_data.get("name","Fondo"),
                                            "image": img, "grid": bd_data["grid"]})
            # Reconstruir sprites dibujados
            for sp_data in data.get("sprites", []):
                if sp_data.get("grid"):
                    w, h = SPRITE_GRID
                    img = grid_to_photoimage(sp_data["grid"], w, h)
                    # buscar sprite con el mismo nombre
                    for s in self.sprites:
                        if s.name == sp_data.get("name"):
                            s.set_image(img)
                            s.image_data = sp_data["grid"]
                            break
            self._refresh_backdrop_list()
            self._refresh_sprite_list()
            self.status.config(text=T[self.lang]["loaded"] + " " + path)
        except Exception as e:
            messagebox.showerror(T[self.lang]["err"], str(e))

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".sc",
            filetypes=[("Scratch Code", "*.sc")])
        if not path: return
        data = {
            "format":"ScratchCode","version":"2.0",
            "language": self.lang,
            "script": self.script_text.get("1.0", tk.END).rstrip("\n"),
            "sprites": [
                {"name": s.name, "x": s.x, "y": s.y,
                 "direction": s.direction, "scale": s.scale,
                 "color": s.color, "visible": s.visible,
                 "grid": s.image_data}
                for s in self.sprites
            ],
            "backdrops": [
                {"name": bd["name"], "grid": bd.get("grid")}
                for bd in self.backdrops
            ],
            "variables": self.variables,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status.config(text=T[self.lang]["saved"] + " " + path)
        except Exception as e:
            messagebox.showerror(T[self.lang]["err"], str(e))

    def clear_script(self):
        self.script_text.delete("1.0", tk.END)
        for s in self.sprites: s.reset()
        self.status.config(text="")

    def stop_script(self):
        self.stop_flag = True

    # ── Ejecución ──
    def run_script(self):
        if self.running: return
        try:
            blocks = parse_script(self.script_text.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror(T[self.lang]["err"], str(e)); return
        if not blocks: return
        for s in self.sprites: s.reset()
        self.running = True; self.stop_flag = False
        self.btn_run.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        threading.Thread(target=self._exec, args=(blocks,), daemon=True).start()

    def _exec(self, blocks):
        try:
            self._run_blocks(blocks)
        finally:
            self.root.after(0, self._on_run_end)

    def _run_blocks(self, blocks):
        for bid, args, body in blocks:
            if self.stop_flag: return
            s = self.current_sprite
            try:
                self._exec_block(bid, args, body, s)
            except Exception as e:
                self.root.after(0, lambda err=e: messagebox.showerror(
                    T[self.lang]["err"], str(err)))
                return

    def _exec_block(self, bid, args, body, s):
        a = args[0] if args else ""
        # Eventos (hats) — no ejecutan al inicio
        if bid in ("when_flag","broadcast","when_receive"): return
        # Movimiento
        if bid == "move":
            v = float(a or 0); self.root.after(0, lambda: s.move(v)); self._sleep(0.15)
        elif bid == "turn_r":
            v = float(a or 0); self.root.after(0, lambda: s.turn(-v)); self._sleep(0.15)
        elif bid == "turn_l":
            v = float(a or 0); self.root.after(0, lambda: s.turn(v)); self._sleep(0.15)
        elif bid == "goto":
            p = a.split()
            x = float(p[0]) if p else 0; y = float(p[1]) if len(p)>1 else 0
            self.root.after(0, lambda: s.goto(x, y)); self._sleep(0.15)
        elif bid == "glide":
            p = a.split()
            secs = float(p[0]) if p else 1
            x = float(p[1]) if len(p)>1 else 0
            y = float(p[2]) if len(p)>2 else 0
            self.root.after(0, lambda: s.glide(secs, x, y))
        elif bid == "point_dir":
            v = float(a or 90)
            self.root.after(0, lambda: s.turn(v - s.direction)); self._sleep(0.15)
        elif bid == "bounce":
            s.direction = (180 - s.direction) % 360
            self.root.after(0, lambda: s.draw()); self._sleep(0.15)
        elif bid == "set_x":
            v = float(a or 0); self.root.after(0, lambda: s.goto(v, s.y)); self._sleep(0.15)
        elif bid == "set_y":
            v = float(a or 0); self.root.after(0, lambda: s.goto(s.x, v)); self._sleep(0.15)
        # Apariencia
        elif bid == "say":
            msg = self._unquote(a); self.root.after(0, lambda: s.say(msg)); self._sleep(1.5)
        elif bid == "say_secs":
            parts = a.rsplit(None, 1); msg = self._unquote(parts[0])
            secs = float(parts[1]) if len(parts)>1 else 2
            self.root.after(0, lambda: s.say(msg)); self._sleep(secs)
            self.root.after(0, s.clear_bubble)
        elif bid == "think":
            msg = self._unquote(a)
            self.root.after(0, lambda: s.say("💭 " + msg)); self._sleep(1.5)
        elif bid == "show":
            self.root.after(0, s.show); self._sleep(0.1)
        elif bid == "hide":
            self.root.after(0, s.hide); self._sleep(0.1)
        elif bid == "change_size":
            v = float(a or 0)
            self.root.after(0, lambda: s.set_scale(s.scale + v)); self._sleep(0.15)
        elif bid == "set_size":
            v = float(a or 100)
            self.root.after(0, lambda: s.set_scale(v)); self._sleep(0.15)
        elif bid == "switch_backdrop":
            if self.backdrops:
                self.root.after(0, lambda: self._set_backdrop(0))
            self._sleep(0.2)
        elif bid == "next_backdrop":
            if self.backdrops:
                def _next():
                    idx = 0
                    for i, bd in enumerate(self.backdrops):
                        if bd.get("image") and self.backdrop_item:
                            pass
                    self._set_backdrop(0)
                self.root.after(0, _next)
            self._sleep(0.2)
        # Control
        elif bid == "wait":
            self._sleep(float(a or 1))
        elif bid == "repeat":
            n = int(float(a or 1))
            for _ in range(n):
                if self.stop_flag: return
                self._run_blocks(body)
        elif bid == "forever":
            while not self.stop_flag:
                self._run_blocks(body)
        elif bid == "if_then":
            if self._eval_bool(a):
                self._run_blocks(body)
        elif bid == "wait_until":
            while not self.stop_flag and not self._eval_bool(a):
                self._sleep(0.05)
        elif bid == "stop":
            if "todos" in a or "all" in a: self.stop_flag = True
            return
        # Sensores
        elif bid == "ask":
            msg = self._unquote(a)
            self.root.after(0, lambda: self._ask_user(msg))
            self._sleep(0.1)
        # Operadores (reporters)
        elif bid in ("add","sub","mul","div","random","join",
                     "touching","timer"): pass
        # Variables
        elif bid == "set_var":
            parts = a.split(None, 1)
            name = parts[0] if parts else "mi_var"
            val = parts[1] if len(parts)>1 else "0"
            self.variables[name] = self._eval_value(val)
        elif bid == "change_var":
            parts = a.split(None, 1)
            name = parts[0] if parts else "mi_var"
            val = self._eval_value(parts[1]) if len(parts)>1 else 1
            self.variables[name] = float(self.variables.get(name, 0)) + float(val)
        # Lápiz
        elif bid == "pen_down":
            self.pen_active = True; self.pen_last = None
        elif bid == "pen_up":
            self.pen_active = False; self.pen_last = None
        elif bid == "pen_clear":
            for ln in self.pen_lines: self.stage.delete(ln)
            self.pen_lines = []
        elif bid == "set_pen_color":
            self.pen_color = a.strip() or "#ff0000"
        elif bid == "set_pen_size":
            self.pen_size = float(a or 2)

    def _ask_user(self, msg):
        ans = simpledialog.askstring("Scratch Code", msg)
        self.variables["respuesta"] = ans or ""

    def _sleep(self, t):
        end = time.time() + t
        while time.time() < end:
            if self.stop_flag: return
            time.sleep(0.02)

    def _on_run_end(self):
        self.running = False
        self.btn_run.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    @staticmethod
    def _unquote(s):
        s = s.strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            return s[1:-1]
        return s

    @staticmethod
    def _eval_value(s):
        s = str(s).strip()
        try: return float(s)
        except ValueError: return s

    def _eval_bool(self, expr):
        expr = str(expr).strip()
        for op in ("=", ">", "<"):
            if op in expr:
                a, b = expr.split(op, 1)
                a = self._eval_value(a); b = self._eval_value(b)
                if op == "=": return a == b
                if op == ">": return a > b
                if op == "<": return a < b
        return False

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().start()
