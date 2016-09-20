import re



class PubMessage(object):
    """
    A message can be parser to something ..
    Example:
        "a new match coming|123"            // publish to all user
        "frank@a new match coming|123"      // publish to one user
        "frank,jack@a new match coming|123" // publish to some user
    """
    def __init__(self, pub_message):
     
        self.__parser(pub_message)



    def __parser(self, pub_message):
        if ':' in pub_message:

            if '@' in pub_message:
                pattern = re.compile(r'(?P<users>.*)@(?P<match_news>.*):(?P<match_id>.*)')
                n = pattern.match(pub_message)
                self.data=  n.groupdict()
            else:
                pattern = re.compile(r'(?P<match_news>.*):(?P<match_id>.*)')
                n = pattern.match(pub_message)
                self.data =  n.groupdict()
        else:
            self.data = {}
        

    @property
    def user(self):
        users = self.data.get('users', 'all')
        if ',' in users:
            return users.split(',')
        else:
            return users
    @property
    def news(self):
        return self.data.get('match_news','No Match News!')
    
    @property
    def match(self):
        return self.data.get('match_id','No Match Id!')
        


class SubMessage(object):
    """
        Example
            "sub#*"             // sub all match
            "sub#123|456|789"   // sub some match 
            "check"             // check current subscribe
            "check#123"         // check if it's has subscribe 
    """

    def __init__(self, sub_message):
        self.sub_message = sub_message
        self.__parser(sub_message)

    def __parser(self, sub_message):
        if '#' in sub_message:

            pattern = re.compile(r'(?P<command>.*)#(?P<match_id>.*)')
            n = pattern.match(sub_message)
            self.data=  n.groupdict()
        else:
            self.data = {}
        

    @property
    def command(self):
        return self.data.get('command', self.sub_message)
    
    @property
    def match(self):
        matchs = self.data.get('match_id','No Match Id!')
        if '|' in matchs:
            return matchs.split('|')
        else:
            return matchs 
        



if __name__ == '__main__':
    sample = "frank,jack@a new football match:7788"
    result = PubMessage(sample)
    print result.data     
    print result.user
    sample = "a new football match:7788"
    result = PubMessage(sample)
    print result.data
    print result.user
    print result.news
    print result.match
    # =============================================
    sample  = "sub#123|456|789"
    result = SubMessage(sample)
    print result.command
    print result.match
    sample  = "sub#123"
    result = SubMessage(sample)
    print result.command
    print result.match
    sample  = "check"
    result = SubMessage(sample)
    print result.command
    print result.match
