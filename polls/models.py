import datetime
import pytz
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import uuid

# Create your models here.
class Poll(models.Model):
    category_choices = (
       ("anime","anime"),
       ("beauty","beauty"),
       ("business & finance", "business & finance"),
       ("education","education"),
       ("entertainment","entertainment"),
       ("fashion","fashion"),
       ("food","food"),
       ("government & Politics","government & politics"),
       ("lifestyle","lifestyle"),
       ("movies","movies"),   
       ("music","music"),
       ("others","others"),
       ("relationships","relationships"),
       ("religion","religion"),
       ("sports","sports"),
       ("technology","technology"),
    )
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "my_poll")
    title = models.CharField(max_length=100, blank = True, null = True)
    category = models.CharField(choices=category_choices, max_length=100)
    image1 = ResizedImageField(size = [320,280], upload_to = "poll_images", force_format = "jpeg", quality = 100, blank = True,  null = True)
    image2 = ResizedImageField(size = [320,280], upload_to = "poll_images", force_format = "jpeg", quality = 100, blank = True,  null = True)
    multiple_option_selection = models.BooleanField(default = False)
    date_created = models.DateTimeField(auto_now_add=True, blank = True, null=True)
    expire = models.DateTimeField(blank = True, null = True)
    public = models.BooleanField(default = True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        return f"{self.title[0:25]}"
    
    def is_expired(self):
        if self.expire:
            current_day = datetime.datetime.now(pytz.utc)
            if current_day < self.expire:
                return False
            else:
                return True
        else:
            return False

    def leading_option(self):
        leader = 0 # keeps track of the number of votes an option has
        leading_option = "" # holds the option with the highest votes
        tie_list = [] #holds the tie options if there are any
        options = self.option.all()

        # checking for the leading option
        for option in options:
            if option.num_of_votes() > leader:
                leader = option.num_of_votes()
                leading_option = option

        # checking if the other options have the same votes as the leading option
        for option in options:
            if option is leading_option:
                pass
            elif option.num_of_votes() == leader:
                tie_list.append(option)

        if tie_list != "":
            tie_list.append(leading_option)
            return tie_list
        else:
            return leading_option


class Poll_Option(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE, related_name="option")
    image = ResizedImageField(size = [320,280], upload_to = "poll_option_images", quality = 100, blank = True, null = True)
    option = models.CharField(max_length=100,blank = True,null=True)

    def __str__(self):
        return self.option
    
    def num_of_votes(self):
        return len(self.votes.all())
    
    def vote_percent(self):
        total_votes = 0
        all_poll_options = self.poll.option.all() # getting all the votes from the other options of the poll this option belongs to
        for option in all_poll_options:
            total_votes+=option.num_of_votes()
        
        current_option_votes = self.num_of_votes()
        try:
            current_option_votes_percentage = round((current_option_votes/total_votes) * 100)
        except:
            current_option_votes_percentage = 0
        return current_option_votes_percentage



class Poll_Vote(models.Model):
    poll_option = models.ForeignKey(Poll_Option,on_delete=models.CASCADE,related_name="votes",blank = True,null = True)
    voter = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "voters")


class Featured_Polls(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="featured_user")
    polls = models.ManyToManyField(Poll)