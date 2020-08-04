import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.forms import model_to_dict
from timeline.models import TimelinePost, TimelineComment
from jsonschema import validate
import jsonschema
from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from utils.encoder import BSONEncoder

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
        validate(instance= request.body, schema=post_schema)
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

    # convert the postid to a string for JSON encoding
    post._id = str(post._id)
    # for the return value, copy the post in a dictionary
    post_deleted = model_to_dict(post)
    post_deleted['comments'] = [str(comment) for comment in post.comments]

    # for each comment
    for comment in post.comments:
        # try to get the comment from the database
        try:
            comment_gotten = TimelineComment.objects.get(_id=ObjectId(comment))
        except:
            print("CommentID: " + comment + " missing from database")
        comment_gotten._id = str(comment_gotten._id)
        comment_response_list.append(model_to_dict(comment_gotten))
        comment_gotten.delete()

    post.delete()
    return JsonResponse({'post': post_deleted, 'comments': comment_response_list})

def get_all_posts_page(request):
    """ retrieve list of restaurants from database """
    posts = TimelinePost.get_all()
    return JsonResponse(json.loads(json.dumps(posts, cls=BSONEncoder)))


def upload_comment_page(request):
    """Upload post into post timeline post table"""
    try:    # validate request
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
    comment._id = str(comment._id)
    return JsonResponse(model_to_dict(comment))


def get_post_by_restaurant_page(request):
    """Retrieve all posts from a restaurant"""
    rest_id = request.GET.get('restaurant_id')
    return JsonResponse(TimelinePost.get_by_restaurant(rest_id))

def delete_comment_page(request):
    """ Deletes comment from database """
    validate(instance=request.body, schema=comment_schema)
    body = json.loads(request.body)
    comment = TimelineComment.objects.get(_id=body["_id"])
    post = TimelinePost.objects.get(_id=comment.post_id)
    post.comments.remove(comment._id)
    post.save(update_fields=["comments"])
    comment.delete()
    return HttpResponse(status=200)
  
  
def get_comment_data_page(request):
    """ Retrieve comment data of given comment from database """
    comment = TimelineComment.objects.get(_id=request.GET.get('_id'))
    comment._id = str(comment._id)
    comment.likes = list(map(str, comment.likes))
    return JsonResponse({'_id': comment._id, 'post_id': comment.post_id, 'user_email': comment.user_email,
                         'likes': comment.likes, 'content': comment.content, 'Timestamp': comment.Timestamp})
