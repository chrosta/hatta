var hatta = function () {
    var hatta = {};

    hatta._parse_date = function (text) {
        /* Parse an ISO 8601 date string. */

        var m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})Z$/.exec(text);
        return new Date(
            Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5], +m[6]));
    };

    hatta._pad2  = function(number) {
        /* Pad a number with zeroes. The result always has 2 digits. */

        return ('00' + number).slice(-2);
    };

    hatta._format_date = function (d) {
        /* Format a date for output. */

        var tz = -d.getTimezoneOffset() / 60;
        if (tz >= 0) {
            tz = "+" + tz;
        }
        return ("" + d.getFullYear() + "-" +
                hatta._pad2(d.getMonth() + 1) + "-" + 
                hatta._pad2(d.getDate()) + " " +
                hatta._pad2(d.getHours()) + ":" +
                hatta._pad2(d.getMinutes()) + " " +
                "GMT" + tz);
    };

    hatta._foreach_tag = function (tag_names, func) {
        tag_names.forEach(function (tag_name) {
            Array.prototype.forEach.call(
                document.getElementsByTagName(tag_name), func);
        });
    };

    hatta.localize_dates = function () {
        /* Scan whole document for UTC dates and replace them with local time versions. */

        hatta._foreach_tag(['abbr'], function (tag) {
            if (tag.className === 'date') {
                var d = hatta._parse_date(tag.getAttribute('title'));
                if (d) {
                    tag.textContent = hatta._format_date(d);
                }
            }
        });
    };

    hatta.js_editor = function () {
        /* Make double click invoke the editor and scroll it to the right place. */

        var textBox = document.getElementById('hatta-editortext');
        if (textBox) {
            /* We have an editor, so scroll it to the right place. */
            var jumpLine = 0 + document.location.hash.substring(1);
            var textLines = textBox.textContent.match(/(.*\n)/g);
            var scrolledText = '';
            for (var i=0, len=textLines.length; i < len && i < jumpLine; ++i) {
                scrolledText += textLines[i];
            }
            /* Put the cursor in the right place. */
            textBox.focus();
            if (textBox.setSelectionRange) {
                textBox.setSelectionRange(scrolledText.length,
                                          scrolledText.length);
            } else if (textBox.createTextRange) {
                var range = textBox.createTextRange();
                range.collapse(true);
                range.moveEnd('character', scrolledText.length);
                range.moveStart('character', scrolledText.length);
                range.select();
            }
            /* Determine the height of our text. */
            var scrollPre = document.createElement('pre');
            textBox.parentNode.appendChild(scrollPre);
            var style = window.getComputedStyle(textBox, '');
            scrollPre.style.font = style.font;
            scrollPre.style.border = style.border;
            scrollPre.style.outline = style.outline;
            scrollPre.style.lineHeight = style.lineHeight;
            scrollPre.style.letterSpacing = style.letterSpacing;
            scrollPre.style.fontFamily = style.fontFamily;
            scrollPre.style.fontSize = style.fontSize;
            scrollPre.style.padding = 0;
            scrollPre.style.overflow = 'scroll';
            try { scrollPre.style.whiteSpace = "-moz-pre-wrap"; } catch(e) {}
            try { scrollPre.style.whiteSpace = "-o-pre-wrap"; } catch(e) {}
            try { scrollPre.style.whiteSpace = "-pre-wrap"; } catch(e) {}
            try { scrollPre.style.whiteSpace = "pre-wrap"; } catch(e) {}
            scrollPre.textContent = scrolledText;
            /* Scroll our editor to the right place. */
            textBox.scrollTop = scrollPre.scrollHeight;
            scrollPre.parentNode.removeChild(scrollPre);
        } else {
            /* We have a normal page, make it go to editor on double click. */
            var baseUrl = '';
            hatta._foreach_tag(['link'], function (tag) {
                if (tag.getAttribute('type') === 'application/wiki') {
                    baseUrl = tag.getAttribute('href');
                }
            });
            if (baseUrl==='') {
                return;
            }
            var dblclick = function () {
                /* The callback that invokes the editor. */
                var url = baseUrl + '#' + this.id.replace('line_', '');
                document.location = url;
                return false;
            };
            hatta._foreach_tag(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'ul',
                          'div'], function (tag) {
                if (tag.id && tag.id.match(/^line_\d+$/)) {
                    tag.ondblclick = dblclick;
                }
            });
        }
    };

    hatta.purple_numbers = function () {
        /* Add links to the headings. */

        hatta._foreach_tag(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], function (tag) {
            var prev = tag.previousSibling;
            while (prev && !prev.tagName) {
                prev = prev.previousSibling;
            }
            if (prev && prev.tagName === 'A') {
                var name = prev.getAttribute('name');
                if (name) {
                    tag.insertAdjacentHTML('beforeend', '<a href="#' +
                        name + '" class="hatta-purple">&para;</a>');
                }
            }
        });
    };

    hatta.toc = function () {
        var tags = [];
        hatta._foreach_tag(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], function (tag) {
            if (tag.getAttribute('id')) {
                tags.push(tag);
            }
        });
        tags.sort(function (a, b) {
            /* Sort according to line numbers from id="line_X" attributes. */
            return a.getAttribute('id').slice(5) - b.getAttribute('id').slice(5);
        });
        console.log(tags);
    };

    hatta._macros = {};

    hatta.register_macro = function(macroName, callback) {
        hatta._macros[macroName] = callback;
    };

    hatta.run_macros = function() {
        for (let macro in hatta._macros) {
            for (let elt of document.getElementsByClassName(macro)) {
                hatta._macros[macro](elt);
            }
        }
    };
    
    hatta.first_letter_as_capital_for_articles_name_hack = function() {
        var article = "";
        var href = window.location.href;
        if (href.indexOf('/+') > 0) {
            if (href.indexOf('/+edit/') > 0) {
                article = /\/[^\/]+$/.exec(href);
                if (article !== null) {
                    article = article[0];
                    if ((/\.[0-9,A-Z,a-z]+$/.exec(article)) === null) {
                        if (article[1] !== article[1].toUpperCase()) {
                            href = href.replace(article, "/" + article[1].toUpperCase() + article.substring(2));
                            window.location.replace(href);
                        }
                    }
                }
            }
        } else {
            if ((/\.[0-9,A-Z,a-z]+$/.exec(href)) === null) {
                var element = document.getElementsByTagName("h1")[0];
                element.innerHTML = element.innerHTML + ".";
            }
        }
    };

    hatta.path_to_article_in_strictly_lower_letters_hack = function() {
        var href = window.location.href;
        var path = /\/.*\//.exec(href.replace(/^.*\/\//, ""));
        if (path !== null) {
            path = path[0];
            var temp = path.replace(/[\W,0-9]/gi, "");
            if (href.indexOf('/+edit/') > 0) {
                for (var i = 0; i < temp.length; i++) {
                    if (temp[i] === temp[i].toUpperCase()) {
                        href = href.replace(path, path.toLowerCase());
                        window.location.replace(href);
                    }
                }
            }
        }
    };

    hatta.content_links_with_brackets_hack = function() {
        var href = window.location.href;
        if (href.indexOf('/+xxx/') > 0) {}
        else {
            var link = "";
            var text = "";
            var content = document.getElementById("hatta-content");
            var regex = /<a[^<]+<\/a>/g;
            var all_links = content.innerHTML.match(regex);
            var unique_links = [];
            if (all_links !== null) {
                for (var i = 0; i < all_links.length; i++) {
                    link = all_links[i];
                    if (unique_links.includes(link) === false) {
                        unique_links.push(link);
                    }
                }
                for (var i = 0; i < unique_links.length; i++) {
                    link = unique_links[i];
                    if (link.indexOf("><") > 0) {}
                    else {
                        if (link.indexOf("~") > 0) {
                            content.innerHTML = content.innerHTML.replaceAll(link, "<span style='font-weight:normal;'>[</span>"+link+"<span style='font-weight:normal;'>]</span>");
                        } else {
                            content.innerHTML = content.innerHTML.replaceAll(link, "<span style='font-weight:normal;'>[</span><b>"+link+"</b><span style='font-weight:normal;'>]</span>");
                        }
                    }
                }
            }
        }
    };

    hatta.item_type_under_page_index_hack = function() {
        var href = window.location.href;
        if (href.indexOf('/+index') > 0) {
            var li_item = "";
            var href_regex = /href=["'][^"']+["']/g;
            var ul_container = document.getElementsByClassName("index")[0];
            for (let i = 0; i < ul_container.children.length; i++) {
                li_item = ul_container.children[i];
                file_extension = /(\.[A-Za-z0-9]+)["']$/.exec(li_item.innerHTML.match(href_regex)[0]);
                if (file_extension !== null) {
                    li_item.innerHTML = li_item.innerHTML.replace("Item ", "File ");
                } else {
                    li_item.innerHTML = li_item.innerHTML.replace("Item ", "Page ");
                }
            }
        }
    }
    
    hatta.browser_tab_title_hack = function () {
        var title = document.getElementsByTagName("title")[0];
        title.innerHTML = title.innerHTML.replace(" - ", ", ") + ".";
        console.log(title);
    }

    return hatta;
}();

window.onload = function () {
    /* Initialize our scripts when the document loads. */
    hatta.first_letter_as_capital_for_articles_name_hack();
    hatta.path_to_article_in_strictly_lower_letters_hack();
    hatta.content_links_with_brackets_hack();
    hatta.item_type_under_page_index_hack();
    hatta.browser_tab_title_hack();
    hatta.run_macros();
    hatta.localize_dates();
    hatta.js_editor();
    hatta.purple_numbers();
};
