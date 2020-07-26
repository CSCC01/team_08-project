import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms import model_to_dict
from timeline.models import TimelinePost, TimelineComment
from jsonschema import validate
import jsonschema
from django.core.exceptions import ObjectDoesNotExist, ValidationError

post_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}

comment_schema = {
    'properties': {
        'post_id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}


def upload_post_page(request):
    """Upload post into post timeline post table"""

    try:  # validate request
        validate(instance=body, schema=post_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)

    post = TimelinePost(**body)
    post.full_clean()
    post.save()
    post._id = str(post._id)
    return JsonResponse(model_to_dict(post))

def delete_post_page(request):
    """
    Delete a post and the connected comments with the given post_id from the database
    Body Entries: post_id
    Returns: Json Document containing the deleted post and its connected comments
    """

    try:
        validate(instance = body, schema = post_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)

    try:
        post = TimelinePost.objects.get(_id= body['post_id'])
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid post_id')

    comments = TimelineComment.objects.Filter(_id= body['post_id'])
    comment_response_list = []
    for comment in comments:
        comment_response_list.append(model_to_dict(comment))
        comment.delete()
    post.delete()
    return JsonResponse({'post' : post, 'comments' : comment_response_list})



def upload_comment_page(request):
    """Upload post into post timeline post table"""

    try:    # validate request
        validate(instance=body, schema=comment_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')
      
    body = json.loads(request.body)

    try:    # validate post
        post = TimelinePost.objects.get(_id=body['post_id'])
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Invalid Post_id')

    # create comment
    comment = TimelineComment(**body)
    comment.full_clean()
    comment.save()
    # update post
    post.comments.append(comment._id)
    post.save()

    comment._id = str(comment._id)
    return JsonResponse(model_to_dict(comment))

def delete_comment_page(request):
    """
    Delete a comment with the given comment_id from the database, remove from the connected post
    Body Entries: post_id, comment_id
    Returns: Json Document containing the deleted comment
    """

    try:    # validate request
        validate(instance=body, schema=comment_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)

    try:    # validate post
        post = TimelinePost.objects.get(_id=body['post_id'])
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Invalid Post_id')

    comment = TimelineComment.objects.get('_id')