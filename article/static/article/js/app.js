$(function () {
    // jQueryコード
    // 時間系フィールドにはbootstrap-datepickerよbootstrap-datetimepickerの利用を推奨します。
    // 参考 https://pypi.org/project/django-tempus-dominus/
    // Bootstrap Datepicker
    $('.dateinput').datepicker({
        todayBtn: 'linked',
        format: 'yyyy-mm-dd',
        language: 'ja',
        autoclose: true,
        todayHighlight: true,
    });
    $('.dateinput').attr('placeholder','YYYY-MM-DD');

    $('.datetimeinput').attr('placeholder','YYYY-MM-DD HH:MM:SS');


    // 入力フォームでリターンキー押下時の送信を無効化
    // ※フィールド１個の時は無効
    $('#myform').on('sumbit', function (e) {
        e.preventDefault();
    })

    // 送信ボタンの２度押しを防止
    $('.save').on('click', function (e) {
        $('.save').addClass('disabled');
        $('#myform').submit();
    })

    // 削除ボタンの２度押しを防止
    $('.delete').on('click', function (e) {
        $('.delete').addClass('disabled');
    })

    // [検索を解除] の表示制御
    //
    // 検索フォーム内の項目が一つでも入力されていたら、検索中と見なし
    // [検索を解除]のボタンを有効化する。
    //
    let conditions = $('#filter').serializeArray();
    $.each(conditions, function () {

        // boolフィールドの検索欄は、デフォルトが「1:不明」なので特別扱い
        if ($('[name=' + this.name + ']').hasClass('nullbooleanselect') && this.value == 1) {
            return;
        }

        // その他の項目はnull,'',0,Falseをもって未入力とみなす。
        if (this.value) {
            $('.filtered').css('visibility', 'visible');
        }
    })

    // ページネーションのレスポンシブ対応
    // jQuery Plugin rPageを利用
    // https://auxiliary.github.io/rpage/
    $(".pagination").rPage();
});



function copyhtml() {
  var t = document.createElement('textarea')
  var input = document.getElementById('editor-main').value
  t.textContent = convertMarkdown( input )
  var b = document.getElementsByTagName('body')[0]
  b.appendChild(t)
  t.select()
  var copy = document.execCommand('copy')
  b.removeChild(t)
  return copy
}

  /**
   * Html形式に変換および連結を行う
   */
function convertMarkdown( text ) {
  text = marked(text)
  return text
    .replace(/ id=".+?"/g,'')
    .replace(/<p><p>/g,'<p>')
    .replace(/<\/p><\/p>/g,'</p>')
    .replace(/<h1>/g,"\n<h1>")
    .replace(/<\/h1>/g,"</h1>\n")
    .replace(/<h2>/g,"\n<h2>")
    .replace(/<\/h2>/g,"</h2>\n")
    .replace(/<h3>/g,"\n<h3>")
    .replace(/<\/h3>/g,"</h3>\n")
    .replace(/<h4>/g,"\n<h4>")
    .replace(/<\/h4>/g,"</h4>\n")
    .replace(/<h5>/g,"\n<h5>")
    .replace(/<\/h5>/g,"</h5>\n")
    .replace(/<h6>/g,"\n<h6>")
    .replace(/<\/h6>/g,"</h6>\n")
    .replace('<!--more-->',"\n<!--more-->\n")
    .replace(/<pre>/g,"\n\n<pre>")
    .replace(/<\/pre>/g,"</pre>\n\n")
    .replace(/<p><a[^>]*?href="(https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)"[^>]*?>(https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)<\/a><\/p>/g,"\n$2\n")
}
