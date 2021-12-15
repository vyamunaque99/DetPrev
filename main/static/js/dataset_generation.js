$("#dataTable td").on("click", function () {
  var $currentTable = $(this).closest("table");
  var index = $(this).index();
  $currentTable.find("td").removeClass("selected");
  $currentTable.find("tr").each(function () {
    $(this).find("td").eq(index).addClass("selected");
  });
});

var columnIndex=0;

(function () {
  const cells = document.querySelectorAll("td");
  cells.forEach((cell) => {
    cell.addEventListener("click", () =>
      columnHandler(cell.cellIndex)
    );
  });
})();

function columnHandler(value){
    columnIndex=value
    console.log(columnIndex);
    $('#js_id_index').val(columnIndex)
};