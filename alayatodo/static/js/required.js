function onSubmit() {
    if (/\S/.test($('#des_id').val())){
        $('#AddModal').modal('show');
        return true;

    } else{
        $('#NoDescModal').modal('show');
        return false;
    }
}