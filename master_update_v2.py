import os
import re

tips = {
    'pt_BR': """**Dica de Navegação:**
- Pressione `Escape` na lista de resultados para voltar à **seleção de provedor**. Se você selecionar um provedor (o mesmo ou outro) e der `Enter`, a pesquisa será repetida automaticamente.
- Pressione `Escape` **novamente** (na seleção de provedor) para voltar ao **campo de edição**.
- **Atalho Rápido:** Se estiver na lista de resultados e quiser voltar instantaneamente para editar sua pesquisa, basta pressionar `Escape` **duas vezes**.""",
    
    'en': """**Navigation Tip:**
- Press `Escape` in the results list to return to **provider selection**. If you select a provider (the same one or a different one) and press `Enter`, the search will be repeated automatically.
- Press `Escape` **again** (at provider selection) to return to the **edit field**.
- **Quick Shortcut:** If you are in the results list and want to instantly return to edit your search, just press `Escape` **twice**.""",
    
    'es': """**Consejo de Navegación:**
- Presione `Escape` en la lista de resultados para volver a la **selección de proveedor**. Si selecciona un proveedor (el mismo u otro) y pulsa `Enter`, la búsqueda se repetirá automáticamente.
- Presione `Escape` **nuevamente** (en la selección de proveedor) para volver al **campo de edición**.
- **Atajo Rápido:** Si está en la lista de resultados y quiere volver instantáneamente para editar su búsqueda, simplemente presione `Escape` **dos veces**.""",
    
    'fr': """**Conseil de Navigation:**
- Appuyez sur `Échap` dans la liste des résultats pour revenir à la **sélection du fournisseur**. Si vous sélectionnez un fournisseur (le même ou un autre) et appuyez sur `Entrée`, la recherche sera répétée automatiquement.
- Appuyez à nouveau sur `Échap` (dans la sélection du fournisseur) pour revenir au **champ d'édition**.
- **Raccourci Rapide:** Si vous êtes dans la liste des résultats et souhaitez revenir instantanément pour modifier votre recherche, appuyez simplement sur `Échap` **deux fois**.""",

    'it': """**Consiglio di Navigazione:**
- Premi `Escape` nella lista dei risultati per tornare alla **selezione del provider**. Se selezioni un provider (lo stesso o un altro) e premi `Invio`, la ricerca verrà ripetuta automaticamente.
- Premi `Escape` **di nuovo** (nella selezione del provider) per tornare al **campo di modifica**.
- **Scorciatoia Rapida:** Se sei nella lista dei risultati e vuoi tornare istantaneamente per modificare la tua ricerca, premi semplicemente `Escape` **due volte**.""",

    'de': """**Navigations-Tipp:**
- Drücken Sie `Escape` in der Ergebnisliste, um zur **Anbieterauswahl** zurückzukehren. Wenn Sie einen Anbieter (denselben oder einen anderen) wählen und `Enter` drücken, wird die Suche automatisch wiederholt.
- Drücken Sie **erneut** `Escape` (bei der Anbieterauswahl), um zum **Bearbeitungsfeld** zurückzukehren.
- **Schnellzugriff:** Wenn Sie sich in der Ergebnisliste befinden und sofort zur Bearbeitung Ihrer Suche zurückkehren möchten, drücken Sie einfach **zweimal** `Escape`.""",

    'ru': """**Совет по навигации:**
- Нажмите `Escape` в списке результатов, чтобы вернуться к **выбору провайдера**. Если вы выберете провайдера (того же или другого) и нажмете `Enter`, поиск повторится автоматически.
- Нажмите `Escape` **еще раз** (в выборе провайдера), чтобы вернуться в **поле редактирования**.
- **Быстрый переход:** Если вы находитесь в списке результатов и хотите мгновенно вернуться к редактированию поиска, просто нажмите `Escape` **дважды**.""",

    'tr': """**Gezinme İpucu:**
- **Sağlayıcı seçimine** dönmek için sonuç listesinde `Escape` tuşuna basın. Bir sağlayıcı (aynısı veya farklısı) seçip `Enter`a basarsanız, arama otomatik olarak tekrarlanır.
- **Düzenleme alanına** dönmek için (sağlayıcı seçiminde) **tekrar** `Escape` tuşuna basın.
- **Hızlı Kısayol:** Sonuç listesindeyseniz ve aramanızı düzenlemek için anında geri dönmek istiyorsanız, sadece **iki kez** `Escape` tuşuna basın.""",

    'ja': """**ナビゲーションのヒント:**
- 結果リストで `Escape` を押すと、**プロバイダー選択**に戻ります。プロバイダー（同じもの、または別のもの）を選んで `Enter` を押すと、検索が自動的に繰り返されます。
- **もう一度** `Escape` を押すと（プロバイダー選択時）、**編集フィールド**に戻ります。
- **クイックショートカット:** 結果リストにいて、検索を編集するために即座に戻りたい場合は、`Escape` を **2回** 押すだけです。""",

    'zh_CN': """**导航提示:**
- 在结果列表中按 `Escape` 返回**提供商选择**。如果您选择提供商（相同的或不同的）并按 `Enter`，搜索将自动重复。
- **再次**按 `Escape`（在提供商选择时）返回**编辑字段**。
- **快速捷径:** 如果您在结果列表中想要立即返回编辑您的搜索，只需按 `Escape` **两次**。""",

    'ar': """**نصيحة التنقل:**
- اضغط `Escape` في قائمة النتائج للعودة إلى **اختيار المزود**. إذا اخترت مزودًا (نفسه أو غيره) وضغطت `Enter`، سيتم تكرار البحث تلقائيًا.
- اضغط `Escape` **مرة أخرى** (في اختيار المزود) للعودة إلى **حقل التحرير**.
- **اختصار سريع:** إذا كنت في قائمة النتائج وتريد العودة فورًا لتعديل بحثك، فقط اضغط `Escape` **مرتين**."""
}

base_path = "addon/doc"

markers_start = {
    'pt_BR': "**Dica de Navegação:**",
    'en': "**Navigation Tip:**",
    'es': "**Consejo de Navegación:**",
    'fr': "**Conseil de Navigation:**",
    'it': "**Consiglio di Navigazione:**",
    'de': "**Navigations-Tipp:**",
    'ru': "**Совет по навигации:**",
    'tr': "**Gezinme İpucu:**",
    'ja': "**ナビゲーションのヒント:**",
    'zh_CN': "**导航提示:**",
    'ar': "**نصيحة التنقل:**"
}

for lang, new_text in tips.items():
    file_path = os.path.join(base_path, lang, "readme.md")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        start_marker = markers_start.get(lang)
        if start_marker and start_marker in content:
            idx_start = content.find(start_marker)
            idx_end = content.find("\n### ", idx_start)
            
            if idx_end != -1:
                new_content = content[:idx_start] + new_text + content[idx_end:]
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated docs for {lang}")
            else:
                 print(f"Could not find end of tip block in {lang}")
        else:
            print(f"Could not find start marker '{start_marker}' in {lang}")


def is_comment(line, filename):
    stripped = line.strip()
    if not stripped.startswith("#"):
        return False
    
    if stripped.startswith("#!"): return False
    if "coding:" in stripped: return False
    if stripped.startswith("#include"): return False
    if filename.endswith(".md") or filename.endswith(".markdown"): return False
    
    return True

files_cleaned = 0
for root, dirs, files in os.walk("."):
    if ".git" in dirs: dirs.remove(".git")
    
    for filename in files:
        if filename in ["rewrite_readmes_impl.py", "master_update.py", "master_update_v2.py", "update_readmes.py", "update_tips.py", "correct_tips.py", "refine_readmes.py", "install_dependencies.sh", "update_results_tip.py"]:
             continue # Don't clean my own temporary scripts or install script (it has instructions)
        
        if "lib/" in root: continue
        
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".py", ".sconstruct", ".sh", ".ini"]:
            full_path = os.path.join(root, filename)
            
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                new_lines = []
                changed = False
                for line in lines:
                    if is_comment(line, filename):
                        changed = True
                        continue
                    new_lines.append(line)
                
                if changed:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Cleaned comments in {full_path}")
                    files_cleaned += 1
            except Exception as e:
                print(f"Error processing {full_path}: {e}")

print(f"Total files cleaned: {files_cleaned}")
