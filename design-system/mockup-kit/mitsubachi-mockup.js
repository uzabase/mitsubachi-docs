/* ============================================================================
 * mitsubachi-ui mockup kit — 最小の挙動スクリプト（依存なし・任意読み込み）
 * ----------------------------------------------------------------------------
 * 「触れるモック」にするための最小限の JS。**独自の JS を書かずにこれを使う**。
 * 見た目は一切持たず、kit のクラス・aria 属性を付け外しするだけ（CSS が見た目を持つ）。
 *
 *   <script src="design-system/mockup-kit/mitsubachi-mockup.js" defer></script>
 *
 * 【属性を付けずに自動で動くもの】
 *   - page-tab / section-tab   … グループ内で --selected と aria-selected を移動
 *   - segmented-control        … --selected を移動（check アイコンを出し入れ）
 *   - filter-chip              … --selected / aria-pressed をトグル（check アイコン）
 *   - switch                   … aria-checked を checked に同期
 *   - table の checkbox 列     … 行の aria-selected を同期・ヘッダーは全選択
 *   - table の th[aria-sort]   … クリックで 昇順 → 降順 → 解除、行を並べ替え
 *   - menu[role=listbox]       … option を選ぶと --selected と check-small を移動
 *
 * 【data 属性で宣言するもの】
 *   <button data-mi-menu="menu-export">…</button>      トリガー（対象 .mi-menu の id）
 *     <div class="mi-menu" id="menu-export" role="menu" hidden>…</div>
 *     ・トリガー基準で「下・左揃え」に出す（menu.md の既定）。外側クリック / ESC で閉じる
 *     ・トリガーに data-mi-menu-label があると、選んだ option のラベルを反映する
 *   <button data-mi-dialog-open="dlg-save">…</button>  ダイアログを開く
 *     <div class="mi-dialog-backdrop" id="dlg-save" hidden>…</div>
 *     ・backdrop の外側クリック / ESC / data-mi-dialog-close を持つ要素で閉じる
 *   <button data-mi-snackbar="保存しました">…</button>  snackbar を出す（4秒で消える）
 *   <button data-mi-tab-panel="panel-1">…</button>     タブに付けるとパネルを切り替える
 *     切り替え対象は data-mi-panel="panel-1" を持つ要素
 *
 * 【この JS でできないこと】
 *   kit に無いコンポーネント（日付選択・アコーディオン等）の挙動は含まない。
 *   必要なら HTML 側に <!-- ds-exception: 理由 --> を書いてから最小限だけ書く。
 * ========================================================================== */
(function () {
  'use strict';

  var SNACKBAR_MS = 4000;

  // --- 小さなヘルパ ---------------------------------------------------------
  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }
  function closest(el, sel) {
    return el && el.closest ? el.closest(sel) : null;
  }
  function show(el) { el.hidden = false; el.style.display = ''; }
  function hide(el) { el.hidden = true; el.style.display = 'none'; }
  function isHidden(el) { return el.hidden || el.style.display === 'none'; }

  /** kit の規則どおりのアイコン span を作る（見た目はクラスが持つ） */
  function icon(name) {
    var s = document.createElement('span');
    s.className = 'mi-icon mi-icon--' + name;
    s.setAttribute('aria-hidden', 'true');
    return s;
  }
  function setIcon(el, name, on) {
    var found = el.querySelector('.mi-icon--' + name);
    if (on && !found) el.appendChild(icon(name));
    if (!on && found) found.remove();
  }

  /** 同じグループ内で修飾子と aria を1つだけに保つ */
  function selectOne(item, groupSel, itemSel, modifier, ariaAttr, iconName) {
    var group = closest(item, groupSel);
    if (!group) return;
    $$(itemSel, group).forEach(function (el) {
      var on = el === item;
      el.classList.toggle(modifier, on);
      if (ariaAttr) el.setAttribute(ariaAttr, on ? 'true' : 'false');
      if (iconName) setIcon(el, iconName, on);
    });
  }

  function isDisabled(el) {
    return el.disabled || el.getAttribute('aria-disabled') === 'true' ||
      el.classList.contains('mi-menu-item--disabled');
  }

  // --- メニュー -------------------------------------------------------------
  var openMenu = null;

  function closeMenu() {
    if (!openMenu) return;
    hide(openMenu.menu);
    if (openMenu.trigger) openMenu.trigger.setAttribute('aria-expanded', 'false');
    openMenu = null;
  }

  /** menu.md の既定「トリガー基準で下・左揃え」。画面下に入らなければ上に出す */
  function placeMenu(menu, trigger) {
    var r = trigger.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.left = Math.round(r.left) + 'px';
    menu.style.top = Math.round(r.bottom + 4) + 'px';
    menu.style.maxHeight = '';
    var m = menu.getBoundingClientRect();
    var margin = 16; // ページ端から 16px 確保（menu.md）
    if (m.bottom > window.innerHeight - margin) {
      if (r.top - m.height - 4 > margin) {
        menu.style.top = Math.round(r.top - m.height - 4) + 'px';
      } else {
        menu.style.maxHeight = Math.round(window.innerHeight - r.bottom - margin - 4) + 'px';
        menu.style.overflowY = 'auto';
      }
    }
    if (m.right > window.innerWidth - margin) {
      menu.style.left = Math.round(Math.max(margin, r.right - m.width)) + 'px';
    }
  }

  function toggleMenu(trigger) {
    var menu = document.getElementById(trigger.getAttribute('data-mi-menu'));
    if (!menu) return;
    var wasOpen = openMenu && openMenu.menu === menu;
    closeMenu();
    if (wasOpen) return;
    show(menu);
    placeMenu(menu, trigger);
    trigger.setAttribute('aria-expanded', 'true');
    openMenu = { menu: menu, trigger: trigger };
  }

  /** listbox の option 選択（select-menu-item のみ selected を持つ） */
  function selectOption(item) {
    var menu = closest(item, '.mi-menu');
    selectOne(item, '.mi-menu', '.mi-menu-item[role="option"]',
      'mi-menu-item--selected', 'aria-selected', 'check-small');
    var trigger = openMenu && openMenu.menu === menu ? openMenu.trigger : null;
    if (trigger && trigger.hasAttribute('data-mi-menu-label')) {
      var label = trigger.querySelector('.mi-menu-label');
      var text = (item.textContent || '').trim();
      if (label) {
        label.textContent = text;
      } else {
        // アイコン等を壊さないよう、最初のテキストノードだけ差し替える
        var node = Array.prototype.find.call(trigger.childNodes, function (n) {
          return n.nodeType === 3 && n.textContent.trim();
        });
        if (node) node.textContent = text;
      }
    }
    closeMenu();
  }

  // --- ダイアログ -----------------------------------------------------------
  function openDialog(id) {
    var backdrop = document.getElementById(id);
    if (!backdrop) return;
    show(backdrop);
    var focusable = backdrop.querySelector(
      '.mi-button, .mi-text-field, .mi-icon-button, [tabindex]');
    if (focusable) focusable.focus();
  }
  function closeDialog(backdrop) {
    if (backdrop) hide(backdrop);
  }

  // --- snackbar -------------------------------------------------------------
  function showSnackbar(message) {
    var vp = document.querySelector('.mi-snackbar-viewport');
    if (!vp) {
      vp = document.createElement('div');
      vp.className = 'mi-snackbar-viewport';
      document.body.appendChild(vp);
    }
    var bar = document.createElement('div');
    bar.className = 'mi-snackbar';
    bar.setAttribute('role', 'status');
    bar.appendChild(icon('check'));
    bar.querySelector('.mi-icon').classList.add('mi-snackbar__icon');
    var p = document.createElement('p');
    p.className = 'mi-snackbar__text';
    p.textContent = message;
    bar.appendChild(p);
    vp.appendChild(bar);
    window.setTimeout(function () { bar.remove(); }, SNACKBAR_MS);
  }

  // --- テーブル -------------------------------------------------------------
  function syncRowSelection(box) {
    var row = closest(box, 'tr');
    if (!row) return;
    if (closest(box, 'thead')) {          // ヘッダー = 全選択
      var table = closest(box, 'table');
      $$('tbody .mi-table__check .mi-checkbox', table).forEach(function (b) {
        b.checked = box.checked;
        var r = closest(b, 'tr');
        if (r) r.setAttribute('aria-selected', box.checked ? 'true' : 'false');
      });
      return;
    }
    row.setAttribute('aria-selected', box.checked ? 'true' : 'false');
    var tbl = closest(box, 'table');
    var head = tbl && tbl.querySelector('thead .mi-table__check .mi-checkbox');
    if (head) {
      var boxes = $$('tbody .mi-table__check .mi-checkbox', tbl);
      var checked = boxes.filter(function (b) { return b.checked; }).length;
      head.checked = checked === boxes.length && boxes.length > 0;
      head.classList.toggle('mi-checkbox--indeterminate',
        checked > 0 && checked < boxes.length);
    }
  }

  var SORT_ICON = { none: 'arrow-up-down', ascending: 'arrow-up-small', descending: 'arrow-down-small' };

  function sortValue(cell) {
    var text = (cell ? cell.textContent : '').trim();
    if (text === '' || text === '–' || text === '-') return null;
    var num = parseFloat(text.replace(/[,\s%億円件人倍]/g, ''));
    return isNaN(num) ? text : num;
  }

  /** table.md: Default → 昇順 → 降順 → 解除 のトグル */
  function sortTable(th) {
    var table = closest(th, 'table');
    var head = closest(th, 'tr');
    var tbody = table.querySelector('tbody');
    if (!tbody || !head) return;
    var index = Array.prototype.indexOf.call(head.children, th);
    var current = th.getAttribute('aria-sort') || 'none';
    var next = current === 'none' ? 'ascending'
      : current === 'ascending' ? 'descending' : 'none';

    $$('thead th[aria-sort]', table).forEach(function (other) {
      if (other === th) return;
      other.setAttribute('aria-sort', 'none');
      Object.keys(SORT_ICON).forEach(function (k) {
        setIcon(other, SORT_ICON[k], SORT_ICON[k] === SORT_ICON.none);
      });
    });
    th.setAttribute('aria-sort', next);
    Object.keys(SORT_ICON).forEach(function (k) {
      setIcon(th, SORT_ICON[k], k === next);
    });

    var rows = $$('tr', tbody);
    if (next === 'none') {
      rows.sort(function (a, b) { return (a._miOrder || 0) - (b._miOrder || 0); });
    } else {
      rows.forEach(function (r, i) { if (r._miOrder == null) r._miOrder = i; });
      var dir = next === 'ascending' ? 1 : -1;
      rows.sort(function (a, b) {
        var x = sortValue(a.children[index]), y = sortValue(b.children[index]);
        if (x === null) return 1;          // 値の無いセルは常に末尾
        if (y === null) return -1;
        if (typeof x === 'number' && typeof y === 'number') return (x - y) * dir;
        return String(x).localeCompare(String(y), 'ja') * dir;
      });
    }
    rows.forEach(function (r) { tbody.appendChild(r); });
  }

  // --- タブ -----------------------------------------------------------------
  function switchTab(tab, groupSel, itemSel, modifier) {
    selectOne(tab, groupSel, itemSel, modifier, 'aria-selected', null);
    var target = tab.getAttribute('data-mi-tab-panel');
    if (!target) return;
    var panels = $$('[data-mi-panel]');
    panels.forEach(function (p) {
      if (p.getAttribute('data-mi-panel') === target) show(p); else hide(p);
    });
  }

  // --- イベント配線 ---------------------------------------------------------
  document.addEventListener('click', function (e) {
    var t = e.target;

    // snackbar は他の data-mi-* と併記できる（例: 閉じてから通知を出す）ため先に処理する
    var snack = closest(t, '[data-mi-snackbar]');
    if (snack) showSnackbar(snack.getAttribute('data-mi-snackbar'));

    var trigger = closest(t, '[data-mi-menu]');
    if (trigger) { e.stopPropagation(); toggleMenu(trigger); return; }

    var opener = closest(t, '[data-mi-dialog-open]');
    if (opener) { openDialog(opener.getAttribute('data-mi-dialog-open')); return; }

    var closer = closest(t, '[data-mi-dialog-close]');
    if (closer) { closeDialog(closest(closer, '.mi-dialog-backdrop')); return; }

    if (t.classList && t.classList.contains('mi-dialog-backdrop')) {
      closeDialog(t); return;                 // 幕の外側クリック
    }

    var option = closest(t, '.mi-menu-item[role="option"]');
    if (option && !isDisabled(option)) { selectOption(option); return; }

    var menuItem = closest(t, '.mi-menu-item');
    if (menuItem) { if (!isDisabled(menuItem)) closeMenu(); return; }

    var pageTab = closest(t, '.mi-page-tab');
    if (pageTab && !isDisabled(pageTab)) {
      switchTab(pageTab, '.mi-page-tab-group', '.mi-page-tab', 'mi-page-tab--selected');
      return;
    }
    var sectionTab = closest(t, '.mi-section-tab');
    if (sectionTab && !isDisabled(sectionTab)) {
      switchTab(sectionTab, '.mi-section-tab-group', '.mi-section-tab', 'mi-section-tab--selected');
      return;
    }

    var segment = closest(t, '.mi-segment');
    if (segment && !isDisabled(segment)) {
      selectOne(segment, '.mi-segmented-control', '.mi-segment',
        'mi-segment--selected', 'aria-checked', 'check');
      return;
    }

    var chip = closest(t, '.mi-chip');
    if (chip && !isDisabled(chip)) {
      var on = !chip.classList.contains('mi-chip--selected');
      chip.classList.toggle('mi-chip--selected', on);
      chip.setAttribute('aria-pressed', on ? 'true' : 'false');
      setIcon(chip, 'check', on);
      return;
    }

    var th = closest(t, 'thead th[aria-sort]');
    if (th) { sortTable(th); return; }

    closeMenu();                              // メニュー外側のクリック
  });

  document.addEventListener('change', function (e) {
    var t = e.target;
    if (!t.classList) return;
    if (t.classList.contains('mi-checkbox') && closest(t, '.mi-table__check')) {
      t.classList.remove('mi-checkbox--indeterminate');
      syncRowSelection(t);
    }
    if (t.classList.contains('mi-switch')) {
      t.setAttribute('aria-checked', t.checked ? 'true' : 'false');
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (openMenu) { closeMenu(); return; }
    var open = $$('.mi-dialog-backdrop').filter(function (b) { return !isHidden(b); });
    if (open.length) closeDialog(open[open.length - 1]);
  });

  // --- 初期化 ---------------------------------------------------------------
  function init() {
    // hidden 属性で隠す指定を、display を持つ kit のクラスにも効かせる
    $$('.mi-dialog-backdrop[hidden], .mi-menu[hidden], [data-mi-panel][hidden]')
      .forEach(function (el) { el.style.display = 'none'; });
    $$('[data-mi-menu]').forEach(function (t) {
      t.setAttribute('aria-expanded', 'false');
      if (!t.hasAttribute('aria-haspopup')) {
        var menu = document.getElementById(t.getAttribute('data-mi-menu'));
        t.setAttribute('aria-haspopup',
          menu && menu.getAttribute('role') === 'listbox' ? 'listbox' : 'menu');
      }
    });
    $$('.mi-table tbody tr').forEach(function (r, i) { r._miOrder = i; });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
