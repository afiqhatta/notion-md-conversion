//(function() {
//
//	// just place a div at top right
//	var div = document.createElement('div');
//	div.style.position = 'fixed';
//	div.style.top = 0;
//	div.style.right = 0;
//	div.textContent = 'Injected!';
//	document.body.appendChild(div);
//
//	alert('inserted self... giggity');
//
//})();

//showCaretPos();

(function(){
    document.body.onkeyup = showCaretPos;
    document.body.onmouseup = showCaretPos;
})();

function setPageBackgroundColor() {
  chrome.storage.sync.get("color", ({ color }) => {
    document.body.style.backgroundColor = color;
  });
}

function addText(){
    document.body.onkeyup = showCaretPos;
    document.body.onmouseup = showCaretPos;
}

//function getSelectionStart() {
//   var node = document.getSelection().anchorNode;
//   return (node.nodeType == 3 ? node.parentNode : node).id;
//}

function showCaretPos() {
    // var el = document.getElementById("test");
    // var caretPosEl = document.getElementById("caretPos");
    // var selectionStart = getSelectionStart()

    // caretPosEl.innerHTML = "Caret position: " + getCaretCharacterOffsetWithin(el) + selectionStart;
    insertTextAtCaret('Hi')
}
//
//function insertTextAtCaret(text) {
//    var sel, range;
//    if (window.getSelection) {
//        sel = window.getSelection();
//        if (sel.getRangeAt && sel.rangeCount) {
//            range = sel.getRangeAt(0);
//            range.deleteContents();
//            range.insertNode( document.createTextNode(text) );
//        }
//    } else if (document.selection && document.selection.createRange) {
//        document.selection.createRange().text = text;
//    }
//}

function insertTextAtCaret(text){
    let selection = window.getSelection();
    let range = selection.getRangeAt(0);
    range.deleteContents();
    let node = document.createTextNode(text);
    range.insertNode(node);

    for(let position = 0; position != text.length; position++)
    {
        selection.modify("move", "right", "character");
    };
}
