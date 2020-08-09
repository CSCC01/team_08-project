import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from timeline.models import TimelinePost, TimelineComment
from jsonschema import validate
import jsonschema
from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from utils.model_util import model_to_json

post_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'user_email': {'type': 'string'},
        'content': {'type': 'string'}
    }
}

comment_schema = {
    'properties': {
        'post_id': {'type': 'string'},
        'user_email': {'type': 'string'},
        'content': {'type': 'string'}
    }
}


def upload_post_page(request):
    """Upload post into post timeline post table"""

    try:  # validate request
        validate(instance=request.body, schema=post_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)
    post = TimelinePost(**body)
    post.full_clean()
    post.save()
    return JsonResponse(model_to_json(post, {'Timestamp': post.Timestamp}))


def delete_post_page(request):
    """
    Delete a post and the connected comments with the given post_id from the database
    Body Entries: post_id
    Returns: Json Document containing the deleted post and its connected comments as
    they were before any deletions took place
    """

    try:  # validate request
        validate(instance=request.body, schema=post_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)

    try:  # try to find the post
        post = TimelinePost.objects.get(_id=body['post_id'])
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid post_id')

    comment_response_list = []
    post_deleted = model_to_json(post)

    # for each comment
    for comment in post.comments:
        # try to get the comment from the database
        try:
            comment_gotten = TimelineComment.objects.get(_id=ObjectId(comment))
        except:
            print("CommentID: " + comment + " missing from database")
        comment_response_list.append(model_to_json(comment_gotten))
        comment_gotten.delete()

    post.delete()
    return JsonResponse({'post': post_deleted, 'comments': comment_response_list})


def get_all_posts_page(request):
    """ retrieve list of restaurants from database """
    posts = list(TimelinePost.objects.all())
    response = {'Posts': []}
    for post in posts:
        time_stamp = {'Timestamp': post.Timestamp.strftime("%b %d, %Y %H:%M")}
        response['Posts'].append(model_to_json(post, time_stamp))
    return JsonResponse(response)

def upload_comment_page(request):
    """Upload post into post timeline post table"""
    try:  # validate request
        validate(instance=request.body, schema=comment_schema)
    except jsonschema.exceptions.ValidationError:
        return HttpResponseBadRequest('Invalid request')

    body = json.loads(request.body)

    try:  # validate post
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
    return JsonResponse(model_to_json(comment))


def get_post_by_restaurant_page(request):
    """Retrieve all posts from a restaurant"""
    rest_id = request.GET.get('restaurant_id')
    posts = list(TimelinePost.objects.filter(restaurant_id=rest_id))
    response = {'Posts': []}
    for post in posts:
        time_stamp = {'Timestamp': post.Timestamp.strftime("%b %d, %Y %H:%M")}
        response['Posts'].append(model_to_json(post, time_stamp))
    return JsonResponse(response)


def delete_comment_page(request):
    """ Deletes comment from database """
    validate(instance=request.body, schema=comment_schema)
    body = json.loads(request.body)
    comment = TimelineComment.objects.get(_id=body["_id"])
    post = TimelinePost.objects.get(_id=comment.post_id)
    remove_comment_from_post(post, comment._id)
    comment.delete()
    return HttpResponse(status=200)


def remove_comment_from_post(post, comment_id):
    """
    Helper function to remove comment from post
    :params-post: associated post
    :params-comment: comment_id to be deleted
    :return: updated post
    """
    post.comments.remove(comment_id)
    post.save(update_fields=['comments'])
    return post


def get_comment_data_page(request):
    """ Retrieve comment data of given comment from database """
    comment = TimelineComment.objects.get(_id=request.GET.get('_id'))
    time_stamp = {'Timestamp': comment.Timestamp.strftime("%b %d, %Y %H:%M")}
    return JsonResponse(model_to_json(comment, time_stamp))
