// activity-processor.js
function toggleReplies(entryId) {
    var replies = document.getElementById('replies-' + entryId);
    var replyForm = document.getElementById('reply-form-' + entryId);
  
    if (replies.style.display === 'none') {
      replies.style.display = 'block';
      replyForm.style.display = 'block';
    } else {
      replies.style.display = 'none';
      replyForm.style.display = 'none';
    }
  }
  