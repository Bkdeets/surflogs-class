from django.db import connection
from .models import Report



class RawOperations:

    # Stored function
    def build_stored_functions(self):
        with connection.cursor() as cursor:
            user_level_function = """CREATE FUNCTION UserLevel(num_sessions int) RETURNS VARCHAR(10)
                                        DETERMINISTIC
                                    BEGIN
                                        DECLARE lvl varchar(10);
                                        IF  num_sessions > 100 THEN SET lvl = 'Tube Hunter';
                                        ELSEIF (num_sessions <= 100 AND num_sessions >= 50) THEN SET lvl = 'Swell Seeker';
                                        ELSEIF (num_sessions < 50 AND num_sessions >= 25) THEN SET lvl = 'Dawn Patroller';
                                        ELSEIF (num_sessions < 25 AND num_sessions >= 10) THEN SET lvl = 'Weekend Warrior';
                                        ELSEIF (num_sessions < 10 AND num_sessions > 1) THEN SET lvl = 'Summer Surfer';
                                        ELSEIF num_sessions < 1 THEN SET lvl = 'Barrel Dodger';
                                        END IF;
                                        RETURN (lvl);
                                    END
                                    """
            try:
                cursor.execute(user_level_function)
                print("Built stored functions")
            except:
                print("Unable to build stored functions")



    # Database views
    def create_usersummarys(self):
        with connection.cursor() as cursor:
            raw_sql = """
                CREATE VIEW logs_usersummary AS
                SELECT user.user_id, user.username, profile.bio, profile.photo, profile.homespot
                FROM profile,user
                WHERE profile.user_id = user.user_id;
            """

            cursor.execute(raw_sql)

            try:
                cursor.execute(raw_sql)
                return 0
            except:
                print("View creation failure")
                return -1

    # Prepared statement and INSERT operation
    def processReportFormAndReturnId(self, report_post_form, user):
        with connection.cursor() as cursor:

            prepared = "INSERT INTO logs_report(date, time, spot_id, user_id, notes, wave_quality) VALUES (DATE(%s),TIME(%s),%s,%s,%s,%s);"
            fields = report_post_form.data

            date = convertDate(fields['date'])
            time = convertTime(fields['time'])

            cursor.execute(prepared,(
                fields['date'],
                fields['time'],
                fields['spot'],
                str(user),
                fields['notes'],
                fields['wave_quality']
            ))
            print("Successfully inserted new report into Report")
            report = Report.objects.filter(user=user)[0]
            #report.date = self.dateTimeConvert(fields['date'])
            report.save()
            return report.report_id

            # try:
            #     cursor.execute(prepared,[
            #         fields['date'],
            #         fields['spot'],
            #         user,
            #         fields['notes'],
            #         fields['wave_quality']
            #     ])
            #     print("Successfully inserted new report into Report")
            #     report = Report.objects.filter(user=fields['user'])[0]
            #     return report.report_id
            # except Exception as e:
            #     print(repr(e))
            #     print("Unable to insert new report into Report")
            #     return -1

    def create_trigger(self):

        sql_string = "DROP TRIGGER new_session_record;"
        with connection.cursor() as cursor:
            cursor.execute(sql_string)

        sql_string = """CREATE TRIGGER new_session_record AFTER INSERT ON logs_session
                        BEGIN
                           INSERT INTO logs_session_record VALUES (new.user_id, new.session_id, datetime('now'), null);
                        END;"""

        with connection.cursor() as cursor:
            cursor.execute(sql_string)

    def execSQL(self,sql,params):
        with connection.cursor() as cursor:
            cursor.execute(sql,params)
            return cursor.fetchall()

    def dateTimeConvert(self,dateString):

        date,time,ampm = dateString.split(" ")
        m,d,y = date.split("/")
        h,m = time.split(":")
        if ampm != "AM":
            h = str(int(h)+12)
        s = "00"

        return f'{y}-{m}-{d} {h}:{m}:{s}'
