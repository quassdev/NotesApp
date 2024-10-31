$(document).ready(function() {
    $('#addNoteButton').click(function() {
        const title = $('#noteTitle').val();
        const content = $('#noteContent').val();

        if (title && content) {
            $('#notesList').append(`<li><strong>${title}</strong>: ${content}</li>`);
            $('#noteTitle').val('');
            $('#noteContent').val('');
        } else {
            alert("Please enter both title and content.");
        }
    });
});
