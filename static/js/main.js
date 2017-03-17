$(function () {
	var $modalEdit = $('#modal-edit');
	var $modalAdd = $('#modal-add');
	var $items = $('.item');
	var $addItem = $('#add-item');

	$('#edit-date-time-picker').datetimepicker({
		sideBySide: true
	});
	$('#add-date-time-picker').datetimepicker({
		sideBySide: true
	});

	$items.on('click', function() {
		$items.removeClass('active');
		$(this).addClass('active');

		$modalEdit.modal();

		$modalEdit.find('.id-item').val(this.id);
		$modalEdit.find('.label-item').val($(this).find('.label-item').text());
		$modalEdit.find('.date-item').val($(this).find('.date-item').text())
	});

	$addItem.on('click', function() {
		$modalAdd.modal();
	});
});