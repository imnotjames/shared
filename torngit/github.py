                user='%(username)s',
        raise gen.Return(commentid)
                                     f.get('previous_filename') or f.get('filename'),
        query = '%srepo:%s+type:pr%s' % (
                (('+state:%s' % state) if state else ''))
            raise gen.Return([(None, str(pr['number'])) for pr in prs['items']])