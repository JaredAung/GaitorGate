const textarea = document.getElementById('chat_text');
const form = document.getElementById('chat-form');

textarea.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault(); // Prevent the default newline behavior
        form.submit();
    }
});