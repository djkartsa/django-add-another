/* django-add-another JS */

/* Modified RelatedObjectLookups.js from Django admin.

    Handles related-objects functionality: lookup link for raw_id_fields
    and Add Another links.

    Customized to work with django-select2.
 */

function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
        href = triggeringLink.href + '&_popup=1';
    } else {
        href = triggeringLink.href + '?_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
}

function showAddAnotherPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
            if ($(elem).hasClass('select2-offscreen')) {
                var data = $(elem).select2('data');
                data = data.concat({id: newId, text: newRepr});
                $(elem).select2('data', data);
            }
        } else if (elemName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else if (!$(elem).hasClass('select2-offscreen')) {
                elem.value = newId;
            }
            else {  // Custom handling for django-select2
                var id = $(elem).attr('id');
                var $select2_elem = $('#s2id_' + id);
                var $realEl = $select2_elem.data().select2.opts.element;

                $realEl.on("select2-loaded.chained", function(e) {
                    $realEl.off("select2-loaded.chained");
                    $select2_elem.select2("close");
                    var results = $(elem).data("results");
                    var selectedObj = $.grep(results, function(e){ return e.id == newId; });
                    $select2_elem.select2("data", selectedObj[0]);
                    $(elem).change();
                });

                $select2_elem.select2("open");
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}

// Add class `input-group` to add-another div elements.
$(function() {
    $('.add-another').parent('div').addClass('input-group')
});