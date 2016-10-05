import os, sys
import click

@click.command()
@click.option('--domain', prompt='Enter your domain name ',  help='Pass your domain name here. For example : example.dev')
@click.option('--path',  prompt='Enter your project path ', help='Pass your project path. For example : /var/www')

def main(domain, path):

    domain_config = domain +".conf"
    vhost_file = "/etc/apache2/sites-available/"+ domain_config
    project_path = path +"/"+ domain

    # if already the project directory is created then exists
    if not os.path.exists(project_path):
        # create the projec path
        os.makedirs( path +"/"+ domain, 0o755 )
        # show the success message
        click.secho('%s directory was created.' % domain,fg='green')
        # create virtual host configuration file
        os.system("touch "+ vhost_file)
        # virtual configuration file permission
        os.system("chmod 0777 "+ vhost_file)

        # Virtual Hosts Configuration
        with open(vhost_file, "a+") as vfile:
            vfile.write("<VirtualHost *:80>\n")
            vfile.write("\tServerAdmin email.example@com\n")
            vfile.write("\tServerName "+ domain +"\n")
            vfile.write("\tServerAlias www."+ domain +"\n")
            vfile.write("\tDocumentRoot "+ project_path +"\n")
            vfile.write("\tErrorLog ${APACHE_LOG_DIR}/error.log\n")
            vfile.write("</VirtualHost>")

        # Given 777 permission to the Virtual Hosts
        os.system("chmod -R 777 /etc/hosts")
        # Virtual Hosts
        with open("/etc/hosts", "a+") as f:
            f.write("\n127.0.0.1 \t "+ domain)

        # virtual host created message
        click.secho('%s virtual host was created.' % vhost_file,fg='green')

        # Enabled this site
        os.system("a2ensite "+ domain_config +" -y")

        # Apache2 reload
        os.system("service apache2 restart -y")
        # Success message
        click.secho("Congratulation, %s successfully created!" % domain,fg='green')
    else:
        click.secho('The directory and virtual host was created!',fg='green')