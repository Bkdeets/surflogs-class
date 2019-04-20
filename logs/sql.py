from django.db import connection
from .models import Report
from django.utils import timezone



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
    def processReportFormAndReturnId(self, report_post_form, user, wave_data):
        with connection.cursor() as cursor:

            prepared = "INSERT INTO logs_report(date, time, spot_id, user_id, notes, wave_quality, wave_data_id) VALUES (%s,%s,%s,%s,%s,%s, %s);"
            fields = report_post_form.data

            date = self.convertDate(str(fields['date']))
            time = self.convertTime(str(fields['time']))

            cursor.execute(prepared,(
                date,
                time,
                fields['spot'],
                str(user),
                fields['notes'],
                fields['wave_quality'],
                str(wave_data)
            ))
            print("Successfully inserted new report into Report")
            report = Report.objects.filter(user=user)[0]
            #report.date = self.dateTimeConvert(fields['date'])
            #report.save()
            return report.report_id

    def convertDate(self, date_string):
        mm,dd,yyyy = date_string.strip().split("/")
        return yyyy+"-"+mm+"-"+dd+" 00:00:00.000000+00:00"

    def convertTime(self, time_string):
        numbers, time_of_day = time_string.strip().split(" ")
        hours, minutes = numbers.split(":")
        if time_of_day == "PM":
            hours = hours + 12
        return hours+":"+minutes+":00.000000+00:00"




    def create_trigger(self):
        sql_string = "DROP TRIGGER new_session_record;"
        with connection.cursor() as cursor:
            cursor.execute(sql_string)

        sql_string = """CREATE TRIGGER new_session_record AFTER INSERT ON logs_session
                        BEGIN
                           INSERT INTO logs_session_record(user_id, session_id, datetime) VALUES (new.user_id, new.session_id, datetime('now'));
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
