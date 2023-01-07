function ChangeColor(item){
      var linenumber = item.getAttribute("line");
      var nowline = document.getElementById(linenumber+"q");
      var text = nowline.querySelector('[tag=unchecked]');
      var blueButtons = nowline.querySelectorAll('button[bgcolor=blue]');

      if (blueButtons) {
        for (var i=0; i<blueButtons.length; i++){
          blueButtons[i].style.backgroundColor = null;
          blueButtons[i].removeAttribute('bgcolor');
        }
      }
      item.style.backgroundColor = '#56C0C0';
      item.setAttribute('bgcolor', 'blue');
      text.style.color = null;
      text.setAttribute('tag', 'checked');
}

function getresult(){
      result = 0;
      var redText = document.querySelectorAll('[tag=unchecked]');
      var blueButtons = document.querySelectorAll('button[bgcolor=blue]');

      for (var j=0; j<redText.length; j++){
              redText[j].style.color = '#AB0000';
          if (j === 0) {
            document.getElementById('res').innerHTML = "Вы ответили не на все вопросы";
          }
            }
      if (redText.length === 0) {
        for (var i=0; i<blueButtons.length; i++){
            result += parseInt(blueButtons[i].value);
          }
        document.getElementById('res').innerHTML = "Набрано баллов: "+result+"";
        document.getElementById('save').innerHTML = "Для сохранения результата введите своё ФИО"+
        "<div><form autocomplete=\"off\" method='post'><input type='text' class='userform' autofocus required name='patient' value='{{request.form.patient}}'><button type=\"submit\" value="+result+" name='result' class='savebutton'>Отправить</button></form></div>"


//        const data = JSON.stringify({
//            "selectedItems": $('#res').val()
//            });
//            $.ajax({
//                url: "/",
//                type: "POST",
//                contentType: "application/json",
//                data: data,
//                success: function (data) {
//                    console.log(data);
//                },
//            });

        }
        }